# importations
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from .predict_functions import add_html_template_to_graph_predict, inv_diff_pred, make_prediction, plot_predict

# creation of the REST API
router = APIRouter(prefix='/predict',
              tags=["predict"],
              responses={404: {"description": "Not found"}}
              )

# HTML templates and CSS files
templates = Jinja2Templates(directory='../templates')
router.mount('/static', StaticFiles(directory='../static'), name='static')


@router.get('/', response_class=HTMLResponse, name="Predictions")
async def predict(request: Request):
    """
    Tune the model, visualize the predictions and analyze the metrics, export a PDF of the results
    """

    data = {'page': 'Predictions'}
    return templates.TemplateResponse('predict.html', {'request': request, 'data': data})


@router.post('/predict_call', response_class=HTMLResponse, name="Make predictions")
async def predict_call(request: Request, nb_period: int = Form(...)):
    """
    Display the evolution of the national demand (ND) during a given time period
    """

    data = {'page': 'Predictions'}
    prediction = make_prediction(nb_period)
    prediction = inv_diff_pred(prediction)
    plot_predict(prediction)
    add_html_template_to_graph_predict('../templates/graph_predictions.html', 'graph_predictions')
    return templates.TemplateResponse('graph_predictions.html', {'request': request, 'data': data})