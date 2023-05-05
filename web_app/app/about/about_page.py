# importations
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

current_directory = os.getcwd()
relative_path_static = "static"
full_path_static = os.path.join(current_directory, relative_path_static)
relative_path_template = "templates"
full_path_template = os.path.join(current_directory, relative_path_template)

# creation of the REST API
router = APIRouter(prefix='/about',
              tags=["about"],
              responses={404: {"description": "Not found"}}
              )

# HTML templates and CSS files
templates = Jinja2Templates(directory=full_path_template)
router.mount('/static', StaticFiles(directory=full_path_static), name='static')

@router.get('/', response_class=HTMLResponse, name="About the project")
async def get_about(request: Request):
    """
    Who are we, what is the purpose of this project, where does it come from?
    """

    data = {'page': 'About this project'}
    return templates.TemplateResponse('about.html', {'request': request, 'data': data})
