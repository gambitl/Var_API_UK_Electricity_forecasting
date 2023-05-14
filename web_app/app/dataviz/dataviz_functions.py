import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import gridplot, row
from bokeh.models import Range1d
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

#df on GCS path
nom_df = 'historic_demand_2009_2023_noNaN.csv'
path_df = os.path.join(gs_path,bucket_name, folder_data, nom_df).replace('\\','/')

relative_path_template = "templates"
full_path_template = os.path.join(current_directory, relative_path_template)

#Creation and formatting of the DataFrame
df = pd.read_csv(path_df)


weekday=pd.to_datetime(df['settlement_date']).dt.weekday
day=pd.to_datetime(df['settlement_date']).dt.day
month=pd.to_datetime(df['settlement_date']).dt.month
year=pd.to_datetime(df['settlement_date']).dt.year
df.insert(1,'weekday',weekday)
df.insert(2,'day',day)
df.insert(3,'month',month)
df.insert(4,'year',year)
df=df.rename({'period_hour':'hour'},axis=1)
df=df.drop(['settlement_date','settlement_period'],axis=1)

#Creation of a lighter DataFrame, grouped by day to ease the visualization on a longer period of time
df_nd_grouped_by_day = df[['day','month','year','nd']]
df_nd_grouped_by_day['date'] = df_nd_grouped_by_day.year.astype('str')+'/'+df_nd_grouped_by_day.month.astype('str')+'/'+df_nd_grouped_by_day.day.astype('str')
df_nd_grouped_by_day = df_nd_grouped_by_day.drop(['day','month','year'],axis=1)
df_nd_grouped_by_day = df_nd_grouped_by_day.groupby('date',sort=False)['nd'].sum().reset_index()

#Create a list of ND values for a specific time period
def create_nd_list(duration):
    if duration == 'day':
        list_index = df.index[:48]
        list_nd=df.nd[:48]
    elif duration == 'week':
        list_index = df.index[528:863]
        list_nd=df.nd[528:863]
    elif duration == 'month':
        list_index = df.index[:1500]
        list_nd=df.nd[:1500]
    elif duration == 'year':
        list_index = range(len(df_nd_grouped_by_day['date'][:365]))
        list_nd = df_nd_grouped_by_day['nd'][:365]
    elif duration == 'full':
        list_index = range(len(df_nd_grouped_by_day['date']))
        list_nd = df_nd_grouped_by_day['nd']
    return (list_index, list_nd)

#Plot the evolution of ND during the selected time period using Bokeh
def plot_time_period(list_index, list_nd, duration):
    output_file(filename =full_path_template+"/graph_time_period.html", title ="Static HTML file")
    p = figure(sizing_mode="stretch_width", max_width=9000, height=500, title=duration)
    line = p.line(list_index, list_nd)
    save(p)

#Add the Jinja2 HTML template blocks inside the HTML graph document
def add_html_template_to_graph_dataset(path, graph):
    #open the file and add the requested templates at the begining
    with open (path, 'r+') as file :
        read_content = file.read()
        file.seek(0, 0)
        file.write('{% extends "dataset.html" %}\n{% block ' + graph + ' %}\n')
        file.write(read_content)
        file.close()
    #open the file and add the requested templates at the end
    with open (path, 'a') as file :
        file.write('\n{% endblock %}')
        file.close()

#Plot the effect of different features on the target using Bokeh
def plot_features_effect(feature):
    #group the dataframe by features
    groups={}
    for i in df[feature].value_counts().keys().sort_values():
        groups[i]=df[df[feature]==i]['nd']
    stats={}
    #determine the statistics for each group
    for i in groups:
        values={}
        values['qmin'], values['q1'], values['q2'], values['q3'], values['qmax'] = groups[i].quantile([0, 0.25, 0.5, 0.75, 1])
        values['iqr'] = values['q3'] - values['q1']
        values['upper'] = values['q3'] + 1.5 * values['iqr']
        values['lower'] = values['q1'] - 1.5 * values['iqr']
        values['mean'] = groups[i].mean()
        values['out'] = groups[i][(groups[i] > values['upper']) | (groups[i] < values['lower'])]
        if not values['out'].empty:
            values['outlier'] = list(values['out'].values)
        stats[i]=values
    #create the boxplots
    figures={}
    weekdays=['mon','tue','wed','thu','fri','sat','sun']
    months=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    holidays=['no','yes']
    for i in groups:
        k=str(i)
        if feature == 'weekday':
            figures[i]= figure(tools="save", x_range= [k], title=weekdays[i], plot_width=100, plot_height=500)
        elif feature == 'month':
            figures[i]= figure(tools="save", x_range= [k], title=months[i-1], plot_width=100, plot_height=500)
        elif feature == 'is_holiday':
            figures[i]= figure(tools="save", x_range= [k], title=holidays[i], plot_width=100, plot_height=500)
        else :
            figures[i]= figure(tools="save", x_range= [k], title=str(i), plot_width=100, plot_height=500)
        upper = min(stats[i]['qmax'], stats[i]['upper'])
        lower = max(stats[i]['qmin'], stats[i]['lower'])    
        hbar_height = (stats[i]['qmax'] - stats[i]['qmin']) / 500    
        figures[i].segment([k], upper, [k], stats[i]['q3'], line_color="black")
        figures[i].segment([k], lower, [k], stats[i]['q1'], line_color="black")    
        figures[i].vbar([k], 0.7, stats[i]['q2'], stats[i]['q3'], line_color="black")
        figures[i].vbar([k], 0.7, stats[i]['q1'], stats[i]['q2'], line_color="black")   
        figures[i].rect([k], lower, 0.2, hbar_height, line_color="black")
        figures[i].rect([k], upper, 0.2, hbar_height, line_color="black") 
        figures[i].y_range = Range1d(0, 60000)   
        if not stats[i]['out'].empty:
            figures[i].circle([k] * len(stats[i]['outlier']), stats[i]['outlier'], size=6, fill_alpha=0.6)
    list_figures=[]
    for i in figures:
        list_figures.append(figures[i])
    #save the boxplots in a html file
    output_file(filename =full_path_template+"/graph_feature.html", title ="Static HTML file")
    save(row(list_figures))

     #"unexpected attribute 'plot_width' to figure, similar attributes are outer_width, width or min_width"