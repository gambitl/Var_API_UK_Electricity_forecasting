#importations
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated

#creation of the REST API
api = FastAPI(title = 'VAR forecasting model deployed on GCP using FastAPI and Docker',
              description = 'web interface powered by FastAPI',
              version = '1.0.0')

#HTML templates and CSS files
templates = Jinja2Templates(directory='../templates')
api.mount('/static', StaticFiles(directory='../static'), name = 'static')

#routes
@api.get('/', response_class=HTMLResponse, name = "Index")
async def get_index(request : Request):
    """
    Display the home page
    """
    data = {'page':'Home page'}
    return templates.TemplateResponse('index.html', {'request' : request, 'data' : data})

@api.get('/dataset', response_class=HTMLResponse, name = "Explore the dataset")
async def dataset(request : Request):
    """
    Use Bokeh to visualize the evolution of the national demand (ND) during a given time period and
    the effect of different features on the target
    """
    data = {'page':'Explore the dataset'}
    return templates.TemplateResponse('dataset.html', {'request' : request, 'data' : data})

@api.post('/duration', response_class=HTMLResponse, name = "ND evolution")
async def duration(request : Request, duration: str = Form(...)):
    """
    Display the evolution of the national demand (ND) during a given time period
    """
    data = {'page':'Explore the dataset'}
    from dataviz import create_nd_list, plot_time_period, add_html_template_to_graph
    list_index, list_nd = create_nd_list(duration)
    plot_time_period(list_index, list_nd)
    add_html_template_to_graph('../templates/graph_time_period.html', 'graph_time_period')
    return templates.TemplateResponse('graph_time_period.html', {'request':request, 'data' : data})

@api.post('/feature', response_class=HTMLResponse, name = "Feature effect")
async def feature(request : Request, feature: str = Form(...)):
    """
    Display the effect of different features on the target (ND)
    """
    data = {'page':'Explore the dataset'}
    from dataviz import create_nd_list, plot_features_effect, add_html_template_to_graph
    list_index, list_nd = create_nd_list(feature)
    plot_features_effect(list_index, list_nd)
    add_html_template_to_graph('../templates/graph_feature.html', 'graph_feature')
    return templates.TemplateResponse('graph_feature.html', {'request':request, 'data' : data})

@api.get('/predict',response_class=HTMLResponse, name = "Make predictions")
async def get_about(request : Request):
    """
    Tune the model, visualize the predictions and analyze the metrics, export a PDF of the results
    """
    data = {'page':'Make predictions'}
    return templates.TemplateResponse('predict.html', {'request' : request, 'data' : data})

@api.get('/about',response_class=HTMLResponse, name = "About the project")
async def get_about(request : Request):
    """
    Who are we, what is the purpose of this project, where does it come from?
    """
    data = {'page':'About this project'}
    return templates.TemplateResponse('about.html', {'request' : request, 'data' : data})