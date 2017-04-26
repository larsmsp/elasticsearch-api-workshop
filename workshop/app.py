# coding=utf-8
import logging

from flask import Flask, request
from flask_cors import CORS

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def hello_world():
    """
    :return: "Hello, world!" til de som besøker siden. 
    """
    return "Hello, world!"


@app.route('/calculator', methods=['GET'])
def calculator():
    """
    Operatorer og operand er angitt i query-parametrene "operator", "operand1" og "operand2", 
    f.eks /calculator?operator=plus&operand1=2&operand2=2
    Endepunktet skal støtte "plus", "minus", "mult" og "div".
    :return: Resultatet av enkle heltallsoperasjoner.
    """
    operand1 = int(request.args['operand1'])
    operand2 = int(request.args['operand2'])
    operator = request.args['operator']
    if operator == 'plus':
        return "The sum is %d" % (operand1 + operand2)
    elif operator == 'minus':
        return "The diff is %d" % (operand1 - operand2)
    elif operator == 'mult':
        return "The product is %d" % (operand1 * operand2)
    elif operator == 'div':
        return "The fraction is %d" % (operand1 / operand2)
    else:
        return "Invalid operator", 400


if __name__ == '__main__':
    app.run()
