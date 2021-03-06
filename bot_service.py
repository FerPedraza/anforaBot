from flask import Flask, request
from flask_cors import CORS
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter
from bot import SmartBot
from unpacking_tar import unpacking_tar
from start_logs import logs
global interpreter,agent,users,B_Client
import os
# desempaqueta ultimo modelo entrenado
unpacking_tar()

path_model = './models/train/'
path_nlu = './models/train/nlu'

BOTANFORA_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_PATH = os.path.join(BOTANFORA_DIR, 'models')
MODELS_TRAIN_PATH = os.path.join(MODELS_PATH, 'train')
NLU_PATH = os.path.join(MODELS_TRAIN_PATH, 'nlu')


agent = Agent.load(MODELS_TRAIN_PATH)
interpreter = RasaNLUInterpreter(NLU_PATH)
Bot=SmartBot()

app = Flask(__name__)
CORS(app)
users = {}

#logs
logs(app)

@app.route('/test', methods=['GET'])
def test():
	return {'response':'It is working'}

@app.route('/webhook', methods=['POST'])
def webhook():
	D = dict(request.json)
	return Bot.get_response(D,interpreter,agent,users)

if __name__ == '__main__':
	app.run(host="127.0.0.1", port=5005, debug=False) #host="0.0.0.0", port=5000, debug=False

