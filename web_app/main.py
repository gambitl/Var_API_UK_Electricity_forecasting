# importations
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.dataviz import dataviz_page
from app.predict import predict_page
from app.about import about_page
import uvicorn, os
# creation of the REST API
api = FastAPI(title='VAR forecasting model deployed on GCP using FastAPI and Docker',
              description='web interface powered by FastAPI',
              version='1.0.0')

current_directory = os.getcwd()
relative_path_static = "templates/static"
full_path_static = os.path.join(current_directory, relative_path_static)
relative_path_template = "templates"
full_path_template = os.path.join(current_directory, relative_path_template)

# HTML templates and CSS files
templates = Jinja2Templates(directory=full_path_template)
api.mount('/static', StaticFiles(directory=full_path_static), name='static')


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


if __name__ == "__main__":
    #la ligne suivante doit être décommentée pour passer sur le cloud
    uvicorn.run(api, port=int(os.environ.get("PORT", 8080)), host="0.0.0.0")

    #la ligne suivante doit être décommentée pour testé en local
    #uvicorn.run(api)