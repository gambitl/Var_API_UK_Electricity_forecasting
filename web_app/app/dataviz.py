import pandas as pd
from bokeh.plotting import figure, output_file, save

#Creation and formatting of the DataFrame
df = pd.read_csv('../database/database.csv')
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
def plot_time_period(list_index, list_nd):
    output_file(filename = "../templates/graph_time_period.html", title = "Static HTML file")
    p = figure(sizing_mode="stretch_width", max_width=9000, height=500)
    line = p.line(list_index, list_nd)
    save(p)

#Add the Jinja2 HTML template blocks inside the HTML graph document
def add_html_template_to_graph(path, graph):
    with open (path, 'r+') as file :
        read_content = file.read()
        file.seek(0, 0)
        file.write('{% extends "dataset.html" %}\n{% block ' + graph + ' %}\n')
        file.write(read_content)
        file.close()
    with open (path, 'a') as file :
        file.write('\n{% endblock %}')
        file.close()

#Plot the effect of different features on the target using Bokeh
def plot_features_effect():
    return "a"