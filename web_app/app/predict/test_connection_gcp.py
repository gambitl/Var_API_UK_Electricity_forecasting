import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import gridplot, row
import os
import gcsfs

gcs = gcsfs.GCSFileSystem(project='formation-mle-dev')
artefacts_bucket = 'dataset-projet-mle-var-forecasting'
folder_data = 'data_for_training_and_predict'
folder_model = 'models'
gs_path = 'gs://'

bucket_name = artefacts_bucket
nom_model = 'modele_var_projet_mle_21032023.pkl'
nom_df = 'historic_demand_2009_2023_noNaN.csv'

model_path = os.path.join(gs_path,bucket_name, folder_model, nom_model).replace('\\','/')
path_df = os.path.join(gs_path,bucket_name, folder_data, nom_df).replace('\\','/')

model = pd.read_pickle(model_path)
df = pd.read_csv(path_df, header=None, sep = ";")

print(df.head())