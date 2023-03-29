import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns


def inv_diff_pred(df_orig, df_forecast, lag, second_diff=False):
    """
    This function allows us to inverse the differencation we applied to our dataset.
    :param df_orig: takes our original dataframe as an input in order to get the name of the columns.
    :param df_forecast: takes the dataframe that was created with the .predict() or .forecast(). This will be the one we will be re-transforming
    :param lag : the lag order used
    :param second_diff: this is where we tell the code to take into account a second differenciation. We do not go further in differenciation since that if you need to differenciate 3 times,
    you might want to look to your data and transform it otherwise...
    :return: a dataframe that has been de-differenciated
    """
    columns = df_orig.columns
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
            df_fc_inv[str(col) + '_1d'] = (df_orig[col].iloc[-1 - lag] - df_orig[col].iloc[-2 - lag]) + df_fc_inv[
                str(col)].cumsum()
            df_fc_inv[str(col) + '_forecast'] = df_orig[col].iloc[-1 - lag] + df_fc_inv[str(col) + "_1d"].cumsum()
        else:
            df_fc_inv[str(col) + '_forecast'] = df_orig[col].iloc[-1 - lag] + df_fc_inv[str(col)].cumsum()
    return df_fc_inv


def plot_predict(df_orig, df_predicted):
    """

    :param df_orig: we take into account the prime dataset in order to extract its columns name
    :param df_predicted: we take into account the predicted data frame in order to take out the values from it
    :return: we will just plot the different columns
    """
    columns = df_orig.columns
    font = {'family': 'normal',
            'weight': 'bold',
            'size': 34}

    plt.rc('font', **font)
    sns.set(style="ticks", context="talk")
    plt.style.use("dark_background")
    fig, axes = plt.subplots(6, 2, figsize=(50, 70), dpi=80)
    df_predicted[columns + '_forecast'].plot(subplots=True, ax=axes, color='r', fontsize=36, legend=True)
    plt.legend(fontsize=36)
    plt.tight_layout()
    plt.show()
