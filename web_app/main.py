# importations
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.dataviz import dataviz_page
from app.predict import predict_page
from app.about import about_page

# creation of the REST API
api = FastAPI(title='VAR forecasting model deployed on GCP using FastAPI and Docker',
              description='web interface powered by FastAPI',
              version='1.0.0')

# HTML templates and CSS files
templates = Jinja2Templates(directory='./templates')
api.mount('/static', StaticFiles(directory='./static'), name='static')


# routes
@api.get('/', response_class=HTMLResponse, name="Index")
async def get_index(request: Request):
    """
    Display the home page
    """

    data = {'page': 'Home page'}
    return templates.TemplateResponse('index.html', {'request': request, 'data': data})


"""
===============================================
Dataset page
===============================================
"""

api.include_router(dataviz_page.router)


"""
===============================================
Prediction page
===============================================
"""
api.include_router(predict_page.router)

"""
===============================================
About page
===============================================
"""

api.include_router(about_page.router)
