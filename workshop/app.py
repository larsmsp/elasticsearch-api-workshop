# coding=utf-8
import logging
import os
import urllib2

from elasticsearch_dsl.connections import connections
from flask import Flask, render_template
from flask_cors import CORS
from model import DocumentIndex

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)


ES_HOSTS_ENV = 'ELASTICSEARCH_HOSTS'
es_hosts = ['10.0.0.10'] if ES_HOSTS_ENV not in os.environ else str(os.environ[ES_HOSTS_ENV]).split(',')


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


@app.route('/create/<string:name>', methods=['POST'])
def create(name):
    if DocumentIndex.exists(name):
        return 'An index with that name already exists.', 409
    if DocumentIndex.create(name):
        return 'Index created', 200
    else:
        return 'Unable to create index', 500


if __name__ == '__main__':
    app.run()
