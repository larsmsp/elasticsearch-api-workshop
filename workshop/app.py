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


# Skal returnere en hilsen til navnet angitt i query-parameteret "name", f.eks /greet?name=My%20Name
@app.route('/greet', methods=['GET'])
def greet():
    pass


# Skal returnere en hilsen til navnet angitt i parameteret "id", f.eks /resource/my-id
@app.route('/resource/<id>', methods=['GET'])
def get_resource(id):
    pass


if __name__ == '__main__':
    app.run()
