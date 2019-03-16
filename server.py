# Packages
from bottle import route, run, request,post
import os

# Local files
from utils import *
from voc import *
from model import *
from hyperparameters import *
from predict import *
from json_encoder import *

@post('/conversation')
def index():
	sentence = request.forms.get('sentence')
	return encode(converse(sentence, None, None, chat, voc))

if os.environ.get('APP_LOCATION') == 'heroku':
	run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
	run(host='localhost', port=8080, debug=True)
