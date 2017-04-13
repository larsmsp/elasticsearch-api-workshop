# coding=utf-8
import logging

from flask import Flask, request
from flask_cors import CORS

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)


# Skal returnere "Hello, world!" tilbake til de som besøker siden.
@app.route('/', methods=['GET'])
def hello_world():
    pass


# Skal returnere resultatet av enkle heltallsoperasjoner.
# Operatorer og operand er angitt i query-parametrene "operator", "operand1" og "operand2", f.eks /greet?operator=plus&operand1=2&operand2=2
# Endepunktet skal støtte "plus", "minus", "mult" og "div".
@app.route('/calculator', methods=['GET'])
def calculator():
    pass


if __name__ == '__main__':
    app.run()
