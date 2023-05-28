#on ne fait pas de test sur les variables etc on y va en bourrin

import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import r2_score, mean_absolute_error
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.stattools import adfuller
from scipy.stats import boxcox
from scipy.special import inv_boxcox

import pickle
import joblib
import mlflow
import os 
os.environ["GCLOUD_PROJECT"] = "formation-mle-dev"

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


def pipeline_var(model, x, y, lag, x_train_orig, n_jour_cible, cible):
    model_fitted_var = model.fit(lag, ic = "aic")
    result_normality = model_fitted_var.test_normality().pvalue #"H0 : les données suivent une loi normale. Si p-value <0.05, on rejette
    result_whiteness = model_fitted_var.test_whiteness(round((len(x) + len(y))/5)).pvalue

    #On choisit dans la formule précédente l = nb_observ/5
    #On calcule la moyenne des résidus (biais) que l'on va ajouter à nos preds

    #df_resid = model_fitted_var.resid
    #mean_resid = df_resid.mean()

    lag_order = model_fitted_var.k_ar
    input_data = x.values[-lag_order:]
    y_predicted = model_fitted_var.forecast(y = input_data, steps = len(y))
    #y_predicted = y_predicted + mean_resid #j'ajoute le biais

    """Pour le moment, nos résidus ne passent pas les tests de normalité et de bruits blancs
    Je ne peux donc pas réaliser d'intervalles de confiance classiques
    """
    #forecast_interval = model_fitted_var.forecast_interval(y = input_data, steps = len(y), alpha = 0.05)
    #df_interval_low = pd.DataFrame.from_records(forecast_interval[0] - forecast_interval[1], columns = df_diff_2.columns)
    #df_interval_up = pd.DataFrame.from_records(forecast_interval[0] + forecast_interval[2], columns = df_diff_2.columns)

    #il faudrait coder ici du conditionnel en cas de changement de metric
    df_predicted = pd.DataFrame(y_predicted, index=y.index, columns=x.columns)

    df_true_results = inv_diff(x_train_orig, df_predicted, n_jour_cible)

    #df_interval_low = inv_diff(df_orig, df_interval_low, n_jour_cible)
    #df_interval_up = inv_diff(df_orig, df_interval_up, n_jour_cible)

    #y_test_predicted = (df_true_results["Variable 1_forecast"].apply(lambda x: inv_boxcox(x,fitted_lambda[0])))
    #Sur la ligne précédente, on va détransformer la transformation cox-box en appliquant "inv boxcox" avec en paramètre le lambda associé

    #y_test_predicted_low = (df_interval_low["Spot PEG DA_forecast"].apply(lambda x: inv_boxcox(x,fitted_lambda[0])))
    #y_test_predicted_up = (df_interval_up["Spot PEG DA_forecast"].apply(lambda x: inv_boxcox(x,fitted_lambda[0])))
    #r2_var = r2_ajusted(r2_score(test_labels, y_test_predicted), x)


    #calcul MAE faux ! doit prendre en compte l'origine
    MAE_var = mean_absolute_error(y[cible], df_true_results[cible+'_forecast'])

    return df_true_results, MAE_var, result_normality, result_whiteness

def main():
    tracking_server_host = "34.163.234.198"
    mlflow.set_tracking_uri(f"http://{tracking_server_host}:5000")
    mlflow.set_registry_uri('gs://mlflow-storage-artifacts-var-project')
    mlflow.set_experiment("test_premier_mlflow")


    experiment_name = "var_test_2"
    if mlflow.get_experiment_by_name(experiment_name) is None:
        experiment_id=mlflow.create_experiment(experiment_name)
    else:
        current_experiment=dict(mlflow.get_experiment_by_name(experiment_name))
        experiment_id=current_experiment['experiment_id']

    with mlflow.start_run(experiment_id=experiment_id):
        if __name__ == "__main__":
            mlflow.statsmodels.autolog() 
            df = pd.read_csv('../dataset/historic_demand_2009_2023_noNaN.csv')
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
            

if __name__ == "__main__":
    main()