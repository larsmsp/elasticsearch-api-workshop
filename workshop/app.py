# coding=utf-8
import logging
import urllib2

from elasticsearch_dsl.connections import connections
from flask import Flask, request, render_template
from flask_cors import CORS
from model import DocumentIndex

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)

# Skal lese ut listen over Elasticsearch-instanser av miljøvariabelen 'ELASTICSEARCH_HOSTS'
# Denne settes i app.yaml
es_hosts = ''


def verify_elasticsearch_connection():
    logging.info("Verifying connection to Elasticsearch host(s)")
    for h in es_hosts:
        logging.info("Checking %s..." % h)
        try:
            urllib2.urlopen('http://%s' % h, timeout=2)
        except urllib2.URLError:
            raise RuntimeError('Unable to to connect to Elasticsearch host %s' % h)
    logging.info("All good!")
    return True


verify_elasticsearch_connection()

connections.create_connection(hosts=es_hosts)
app = Flask(__name__)
CORS(app)


@app.route('/')
def root():
    return render_template('root.html',
                           elasticsearch_status='Connected' if verify_elasticsearch_connection() else 'Not connected')

'''
Metoden 'create' skal opprett en indeks med navnet angitt i 'name'.
Den skal svare på endepunktet /create/<navn på indeks> og med HTTP-metode 'PUT'
'''
def create(name):
    pass


if __name__ == '__main__':
    app.run()
