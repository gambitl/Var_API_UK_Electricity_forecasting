# importations
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# creation of the REST API
router = APIRouter(prefix='/about',
              tags=["about"],
              responses={404: {"description": "Not found"}}
              )

# HTML templates and CSS files
templates = Jinja2Templates(directory='../templates')
router.mount('/static', StaticFiles(directory='../static'), name='static')

@router.get('/', response_class=HTMLResponse, name="About the project")
async def get_about(request: Request):
    """
    Who are we, what is the purpose of this project, where does it come from?
    """

    data = {'page': 'About this project'}
    return templates.TemplateResponse('about.html', {'request': request, 'data': data})
