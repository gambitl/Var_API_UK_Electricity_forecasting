# importations
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from .dataviz_functions import create_nd_list, plot_time_period, add_html_template_to_graph_dataset, plot_features_effect


current_directory = os.getcwd()
relative_path_static = "templates/static"
full_path_static = os.path.join(current_directory, relative_path_static)
relative_path_template = "templates"
full_path_template = os.path.join(current_directory, relative_path_template)


# creation of the REST API
router = APIRouter(prefix='/dataviz',
              tags=["dataviz"],
              responses={404: {"description": "Not found"}}
              )

# HTML templates and CSS files
templates = Jinja2Templates(directory=full_path_template)
router.mount('/static', StaticFiles(directory=full_path_static), name='static')


@router.get('/', response_class=HTMLResponse, name="Explore the dataset")
async def landing(request: Request):
    """
    Use Bokeh to visualize the evolution of the national demand (ND) during a given time period and
    the effect of different features on the target
    """

    data = {'page': 'Explore the dataset'}
    return templates.TemplateResponse('dataset.html', {'request': request, 'data': data})



@router.post('/duration', response_class=HTMLResponse, name="ND evolution")
async def duration(request: Request, duration: str = Form(...)):
    """
    Display the evolution of the national demand (ND) during a given time period
    """

    data = {'page': 'Explore the dataset'}
    list_index, list_nd = create_nd_list(duration)
    plot_time_period(list_index, list_nd, duration)
    add_html_template_to_graph_dataset(full_path_template + '/graph_time_period.html', 'graph_time_period')
    return templates.TemplateResponse('graph_time_period.html', {'request': request, 'data': data})



@router.post('/feature', response_class=HTMLResponse, name="Feature effect")
async def feature(request: Request, feature: str = Form(...)):
    """
    Display the effect of different features on the target (ND)
    """

    data = {'page': 'Explore the dataset'}
    plot_features_effect(feature)
    add_html_template_to_graph_dataset(full_path_template + '/graph_feature.html', 'graph_feature')
    return templates.TemplateResponse('graph_feature.html', {'request': request, 'data': data})