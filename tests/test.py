import requests
import os
from datetime import datetime
import pandas as pd

api_address = '127.0.0.1'
api_port = 8000

'''
Tests en 3 parties:
* Test des retours HTML sur chaque endpoint de l'API
* Test de la validité statistique des données (sur la variable cible ND) en comparaison avec les anciennes données
* Test de la qualité des données 
'''

#Test des codes html reçus par les différents endpoints

endpoints = ['', 'dataset', 'predict', 'about']

current_datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

for endpoint in endpoints:
    r = requests.get(url = 'http://{address}:{port}/{endpoint}'.format(address = api_address, 
                                                                       port = api_port, 
                                                                       endpoint = endpoint))
    output = '''
    ENDPOINT TEST
    test_date = {current_datetime}

    request done at "/{endpoint}"
    expected_result = 200
    actual_result = {status_code}

    => {test_status}

    ==============================
    '''
    
    status_code = r.status_code

    if status_code == 200:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'
    
    #Impression dans la sortie standard

    print(output.format(current_datetime = current_datetime,
                        endpoint = endpoint,
                        status_code = status_code,
                        test_status = test_status))
    
    #Enregistrement dans le fichier de logs

    with open ('./api_tests.log', 'a') as file:
        file.write(output.format(current_datetime = current_datetime,
                                 endpoint = endpoint,
                                 status_code = status_code,
                                 test_status = test_status))

#Test de la validité statistique des données

#Construction du dataframe test à partir du dataset actualisé
df_test = pd.read_csv('../dataset/historic_demand_2009_2023_noNaN.csv')

#Construction du dataframe log à partir du fichier csv
df_log = pd.read_csv('./database_tests.csv')

#Actualisation des paramètres dans le dataframe log
list_statistics = []

list_statistics.append(current_datetime)
list_statistics.append(round(df_test['nd'].mean(),2))
list_statistics.append(round(df_test['nd'].median(),2))
list_statistics.append(round(df_test['nd'].min(),2))
list_statistics.append(round(df_test['nd'].max(),2))
list_statistics.append(round(df_test['nd'].std(),2))

df_log.loc[len(df_log.index)] = list_statistics

df_log.to_csv('./database_tests.csv', index = False)

for new_stat, old_stat, stat_name in zip (df_log.iloc[-1][1:], df_log.iloc[-2][1:], df_log.iloc[-1][1:].index):
    output = '''
    DATASET STATISTICAL TEST
    test_date = {current_datetime}

    Control of {stat_name} variation
    old_value = {old_stat}
    new_value = {new_stat}
    expected_variation = +/- 10.0%
    actual_result = {test_value}%

    => {test_status}

    ==============================
    '''

    #Contrôle de la variation à +/- 10%
    test_value = round(100 - ((int(old_stat) / int(new_stat)) * 100),1)
    
    if test_value < 10 and test_value > -10:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    #Impression dans la sortie standard

    print (output.format(old_stat = old_stat,
                         new_stat = new_stat,
                         stat_name = stat_name,
                         current_datetime = current_datetime,
                         test_value = test_value,
                         test_status = test_status,))

    #Enregistrement dans le fichier de logs

    with open ('./api_tests.log', 'a') as file:
        file.write(output.format(old_stat = old_stat,
                                 new_stat = new_stat,
                                 stat_name = stat_name,
                                 current_datetime = current_datetime,
                                 test_value = test_value,
                                 test_status = test_status,))

#Test de la qualité du dataset, contrôle des valeurs manquantes

df_nan = df_test.isna().sum()

output = '''
    DATASET QUALITY TEST
    test_date = {current_datetime}

    Control of missing values
    expected_result = list of 0
    actual_result = {test_values}

    => {test_status}

    ==============================
'''
  
if all(i == 0 for i in df_nan.values):
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'

#Impression dans la sortie standard

print(output.format(current_datetime = current_datetime,
                        test_values = df_nan.values,
                        test_status = test_status))

#Enregistrement dans le fichier de logs

with open ('./api_tests.log', 'a') as file:
    file.write(output.format(current_datetime = current_datetime,
                             test_values = df_nan.values,
                             test_status = test_status))

#Test de la qualité du dataset, contrôle des duplicats

df_duplicated = df_test.duplicated().sum()

output = '''
    DATASET QUALITY TEST
    test_date = {current_datetime}

    Control of duplicated values
    expected_result = 0
    actual_result = {test_values}

    => {test_status}

    ==============================
'''
  
if df_duplicated == 0:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'

#Impression dans la sortie standard

print(output.format(current_datetime = current_datetime,
                    test_values = df_duplicated,
                    test_status = test_status))

#Enregistrement dans le fichier de logs

with open ('./api_tests.log', 'a') as file:
    file.write(output.format(current_datetime = current_datetime,
                             test_values = df_duplicated,
                             test_status = test_status))