
import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error
import datetime

from statsmodels.tsa.vector_ar.var_model import VAR

import airflow
import mlflow
import airflow
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.google.cloud.hooks.compute_ssh import ComputeEngineSSHHook
from airflow.operators.python import PythonOperator
import os 
import gcsfs

import time


os.environ["GCLOUD_PROJECT"] = "formation-mle-dev"
#defining the gcp path
gcs = gcsfs.GCSFileSystem(project='formation-mle-dev')
artefacts_bucket = 'dataset-projet-mle-var-forecasting'
folder_data = 'gcs/data'
folder_model = 'models'
gs_path = 'gs://'
bucket_name = artefacts_bucket
nom_df = "historic_demand_2009_2023_noNaN.csv"



#VM path
GCE_INSTANCE = "vm-mlflow-server"
GCE_ZONE = "europe-west9-a"
GCP_PROJECT_ID = "formation-mle-dev"

#functions
def inv_diff(df_orig, df_forecast, n_jour_cible, second_diff = False):
    columns = df_orig.columns
    df_fc_inv = df_forecast.copy()
    for col in columns:
        """
        Attention ! lorsque l'on inverse une différenciation, un récupère la "dernière donnée" à laquelle on rajoute
        la somme cumulée des valeurs différenciées.
        Dans le cas d'un array prédit, le dernier point de donnée n'est PAS le "-1" du train_set, mais le "-1-nb_jour_pred"
        Dans notre cas on va donc retourner 120 jours en arrière
        Dans le cas d'une double diff, on soustrait d'abord l'avant dernière valeur à la dernière
        """
        if second_diff:
            df_fc_inv[str(col)+'_1d'] = (df_orig[col].iloc[-n_jour_cible-1]-df_orig[col].iloc[-n_jour_cible-2]) + df_fc_inv[str(col)].cumsum()
            df_fc_inv[str(col)+'_forecast'] = df_orig[col].iloc[-n_jour_cible-1] + df_fc_inv[str(col)+"_1d"].cumsum()
        else:
            df_fc_inv[str(col)+'_forecast'] = df_orig[col].iloc[-n_jour_cible-1] + df_fc_inv[str(col)].cumsum()
    return df_fc_inv

def train_model():
    #allow the connexion to take effect
    time.sleep(360)
    #mlflow param
    tracking_server_host = "34.163.234.198"
    mlflow.set_tracking_uri(f"http://{tracking_server_host}:5000")
    mlflow.set_registry_uri('gs://mlflow-storage-artifacts-var-project')
    mlflow.set_experiment("var_test_airflow")
    experiment_name = "var_test_airflow"

    if mlflow.get_experiment_by_name(experiment_name) is None:
        experiment_id=mlflow.create_experiment(experiment_name)
    else:
        current_experiment=dict(mlflow.get_experiment_by_name(experiment_name))
        experiment_id=current_experiment['experiment_id']

    with mlflow.start_run(experiment_id=experiment_id):
        mlflow.statsmodels.autolog() 
        
        cwd = os.getcwd()
        path_csv = os.path.join(cwd, folder_data, nom_df)
        df = pd.read_csv(path_csv)
        df['settlement_date'] = pd.to_datetime(df['settlement_date'])
        df = df.set_index('settlement_date')
        df = df.drop(['settlement_period', 'period_hour'], axis = 1)
        variable_cible = df["tsd"]
        index_df = df.index

        n_period_predict = 48 * 7
        mask = (df.index > '2022-01-01')
        df_pour_var = df.loc[mask]

        df_pour_var = df_pour_var +1

        df_diff_1 = df_pour_var.diff().dropna()

        df_diff_1 = df_diff_1.drop('embedded_solar_capacity', axis = 1)
        df_pour_var = df_pour_var.drop('embedded_solar_capacity', axis = 1)
        df_diff_1 = df_diff_1.drop('is_holiday', axis = 1)
        df_pour_var = df_pour_var.drop('is_holiday', axis = 1)
        df_diff_1 = df_diff_1.drop('embedded_wind_capacity', axis = 1)
        df_pour_var = df_pour_var.drop('embedded_wind_capacity', axis = 1)
        df_diff_1 = df_diff_1.drop('non_bm_stor', axis = 1)
        df_pour_var = df_pour_var.drop('non_bm_stor', axis = 1)

        train_var = df_diff_1[:-n_period_predict]
        test_var = df_diff_1[-n_period_predict:]

        maxlag = 48*7
        train_var.values[-maxlag:].shape
        model_var = VAR(endog = train_var)
        model_var = model_var.fit(48, ic = "aic")
        result_normality = model_var.test_normality().pvalue #"H0 : les données suivent une loi normale. Si p-value <0.05, on rejette
        result_whiteness = model_var.test_whiteness(round((len(train_var) + len(test_var))/5)).pvalue

        lag_order = model_var.k_ar
        input_data = train_var.values[-lag_order:]
        y_predicted = model_var.forecast(y = input_data, steps = len(test_var))

        df_predicted = pd.DataFrame(y_predicted, index=test_var.index, columns=train_var.columns)

        df_true_results = inv_diff(df_pour_var, df_predicted, n_period_predict)

        MAE_var = mean_absolute_error(df_pour_var[variable_cible.name].iloc[-n_period_predict:], df_true_results[variable_cible.name+'_forecast'])
        mlflow.log_metric('MAE', MAE_var)
        mlflow.statsmodels.log_model(model_var, 'model')

#dag
my_dag_train = airflow.DAG(
    dag_id="dag_training_var",
    description='dag that enable the proxy for mlflow server then train the model',
    start_date=datetime.datetime(2023, 5, 25, 9),
    schedule_interval="@hourly"
)

connexion_proxy = SSHOperator(
    task_id='connexion_to_vm',
    ssh_hook=ComputeEngineSSHHook(
        user = "victordistefano2",
          instance_name=GCE_INSTANCE,
          zone=GCE_ZONE,
          project_id=GCP_PROJECT_ID,
          use_oslogin=False,
          use_iap_tunnel=False,
          use_internal_ip=True),
    command="./cloud-sql-proxy --private-ip formation-mle-dev:europe-west9:mlflow-postgres-database",
    retries=0,
    cmd_timeout = 72000,
    conn_timeout = 7200,
    dag = my_dag_train
)

training_task = PythonOperator(
    task_id='training',
    dag=my_dag_train,
    python_callable=train_model,
    trigger_rule="none_skipped"
)
