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


# Skal returnere summen av tallene angitt i query-parametrene "operand1" og operand2, f.eks /greet?operand1=2&operand2=2
@app.route('/add', methods=['GET'])
def add():
    pass


if __name__ == '__main__':
    app.run()
