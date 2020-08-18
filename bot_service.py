from flask import Flask, request
from flask_cors import CORS
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter
from bot import SmartBot
import logging.handlers
from start_logs import logs
global interpreter,agent,users,B_Client

path_model = './models/train/'
path_nlu = './models/train/nlu'

agent = Agent.load(path_model)
interpreter = RasaNLUInterpreter(path_nlu)
Bot=SmartBot()

app = Flask(__name__)
CORS(app)
users = {}

#logs
logs()

@app.route('/test', methods=['GET'])
def test():
	return {'response':'It is working'}

@app.route('/webhook', methods=['POST'])
def webhook():
	D = dict(request.json)
	return Bot.get_response(D,interpreter,agent,users)

if __name__ == '__main__':
	app.run(host="127.0.0.1", port=5000, debug=True)

