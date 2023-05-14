
# %%
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import gridplot, row
import os
import gcsfs

#defining the gcp path
gcs = gcsfs.GCSFileSystem(project='formation-mle-dev')
artefacts_bucket = 'dataset-projet-mle-var-forecasting'
folder_data = 'data_for_training_and_predict'
folder_model = 'models'
gs_path = 'gs://'
bucket_name = artefacts_bucket

current_directory = os.getcwd()
#saved model path
nom_model = 'modele_var_projet_mle_21032023.pkl'
model_path = os.path.join(gs_path,bucket_name, folder_model, nom_model).replace('\\','/')

#df on GCS path
nom_df = 'historic_demand_2009_2023_noNaN.csv'
path_df = os.path.join(gs_path,bucket_name, folder_data, nom_df).replace('\\','/')

relative_path_static = "templates/static"
full_path_static = os.path.join(current_directory, relative_path_static)

relative_path_template = "templates"
full_path_template = os.path.join(current_directory, relative_path_template)

model = pd.read_pickle(model_path)
df = pd.read_csv(path_df)
df['settlement_date'] = pd.to_datetime(df['settlement_date'])
df = df.set_index('settlement_date')
df = df.drop(['settlement_period', 'period_hour', 'embedded_solar_capacity', 'is_holiday', 'embedded_wind_capacity',
              'non_bm_stor'], axis=1)
df_1 = df.diff().dropna()
lag_order = model.lag_order = model.k_ar


def make_prediction(nb_period):
    pred = model.forecast(y=df_1.values[-lag_order:], steps=nb_period)
    pred = pd.DataFrame(pred, columns=df_1.columns)

    return pred


def inv_diff_pred(df_forecast, second_diff=False):
    """
    This function allows us to inverse the differencation we applied to our dataset.
    :param df_orig: takes our original dataframe as an input in order to get the name of the columns.
    :param df_forecast: takes the dataframe that was created with the .predict() or .forecast(). This will be the one we will be re-transforming
    :param lag : the lag order used
    :param second_diff: this is where we tell the code to take into account a second differenciation. We do not go further in differenciation since that if you need to differenciate 3 times,
    you might want to look to your data and transform it otherwise...
    :return: a dataframe that has been de-differenciated
    """
    columns = df.columns
    df_fc_inv = df_forecast.copy()
    for col in columns:
        """
        Warning ! When we "reverse" a differenciation, we take back the last data point of our DF, to which we add the cumulated sum of the differenciated values.
        In the case of a predicted array, the last data point is NOT the '-1' from the train set, but the '-1_nb_days_predicted'
        Dans le cas d'un array prédit, le dernier point de donnée n'est PAS le "-1" du train_set, mais le "-1-nb_jour_pred"
        Dans notre cas on va donc retourner 120 jours en arrière
        Dans le cas d'une double diff, on soustrait d'abord l'avant dernière valeur à la dernière
        """
        if second_diff:
            df_fc_inv[str(col) + '_1d'] = (df[col].iloc[-1 - lag_order] - df[col].iloc[-2 - lag_order]) + df_fc_inv[
                str(col)].cumsum()
            df_fc_inv[str(col) + '_forecast'] = df[col].iloc[-1 - lag_order] + df_fc_inv[str(col) + "_1d"].cumsum()
        else:
            df_fc_inv[str(col) + '_forecast'] = df[col].iloc[-1 - lag_order] + df_fc_inv[str(col)].cumsum()
    return df_fc_inv


def plot_predict(df_predicted):
    """

    :param df_orig: we take into account the prime dataset in order to extract its columns name
    :param df_predicted: we take into account the predicted data frame in order to take out the values from it
    :return: we will just plot the different columns
    """
    # columns = df.columns
    # font = {'family': 'normal',
    #         'weight': 'bold',
    #         'size': 34}
    #
    # plt.rc('font', **font)
    # sns.set(style="ticks", context="talk")
    # plt.style.use("dark_background")
    # fig, axes = plt.subplots(6, 2, figsize=(50, 70), dpi=80)
    # df_predicted[columns + '_forecast'].plot(subplots=True, ax=axes, color='r', fontsize=36, legend=True)
    # plt.legend(fontsize=36)
    # plt.tight_layout()
    # plt.show()
    output_file(filename=full_path_template+"/graph_predictions.html", title="Static HTML file")
    p = figure(sizing_mode="stretch_width", max_width=9000, height=500)
    index = df_predicted.index
    nd = df_predicted['nd_forecast']
    line = p.line(index, nd)
    save(p)
    
def add_html_template_to_graph_predict(path, graph):
    #open the file and add the requested templates at the begining
    with open(path, 'r+') as file :
        read_content = file.read()
        file.seek(0, 0)
        file.write('{% extends "predict.html" %}\n{% block ' + graph + ' %}\n')
        file.write(read_content)
        file.close()
    #open the file and add the requested templates at the end
    with open(path, 'a') as file :
        file.write('\n{% endblock %}')
        file.close()
