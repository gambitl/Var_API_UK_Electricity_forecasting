import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

def inv_diff_pred(df_orig, df_forecast, second_diff = False):
    """
    This function allows us to inverse the differencation we applied to our dataset.
    :param df_orig: takes our original dataframe as an input in order to get the name of the columns.
    :param df_forecast: takes the dataframe that was created with the .predict() or .forecast(). This will be the one we will be re-transforming
    :param second_diff: this is where we tell the code to take into account a second differenciation. We do not go further in differenciation since that if you need to differenciate 3 times,
    you might want to look to your data and transform it otherwise...
    :return: a dataframe that has been de-differenciated
    """
    columns = df_orig.columns
    df_fc_inv = df_forecast.copy()
    for col in columns:
        """
        Warning ! When we "reverse" a differenciation, we take back the last data point of our DF, to which we add the cumulated sum of the differenciated values.
        In the case of a predicted array, the last data point is NOT the 
        Attention ! lorsque l'on inverse une différenciation, un récupère la "dernière donnée" à laquelle on rajoute
        la somme cumulée des valeurs différenciées.
        Dans le cas d'un array prédit, le dernier point de donnée n'est PAS le "-1" du train_set, mais le "-1-nb_jour_pred"
        Dans notre cas on va donc retourner 120 jours en arrière
        Dans le cas d'une double diff, on soustrait d'abord l'avant dernière valeur à la dernière
        """
        if second_diff:
            df_fc_inv[str(col)+'_1d'] = (df_orig[col].iloc[-1]-df_orig[col].iloc[-2]) + df_fc_inv[str(col)].cumsum()
            df_fc_inv[str(col)+'_forecast'] = df_orig[col].iloc[-1] + df_fc_inv[str(col)+"_1d"].cumsum()
        else:
            df_fc_inv[str(col)+'_forecast'] = df_orig[col].iloc[-1] + df_fc_inv[str(col)].cumsum()
    return df_fc_inv