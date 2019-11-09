'''' Entry script for python server '''
from bottle import route, run, request,post
import os

from src.utils import init_logger, json_encode
from src.model import DialoGPT

model = None

@post('/conversation')
def index():
    sentence = request.forms.get('text', '')
    nxt = request.forms.get('next', '')
    if nxt:
        return json_encode(model.GetNext())
    else:
        return json_encode(model.GenerateFor(sentence))

if __name__ == '__main__':
    logger = init_logger('DawnPy')
    model_path = os.path.join(os.getcwd(), 'models', 'medium_ft.pkl')
    model = DialoGPT(model_path)
    if not model.Initialize():
        logger.error('Failed to load model')
        exit(1)
    # print(model.GenerateFor('Hello who are you doing'))
    if os.environ.get('APP_LOCATION') == 'LOCAL':
        run(host='localhost', port=8080, debug=True)
    else:
        run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
