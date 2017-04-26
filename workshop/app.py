# coding=utf-8
import logging
import os
import urllib
import urllib2

from elasticsearch.client import Elasticsearch
from elasticsearch_dsl.connections import connections
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

from model import Document
from model.Document import create_document
from helper import DocumentIndex, Results

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)


ES_HOSTS_ENV = 'ELASTICSEARCH_HOSTS'
es_hosts = ['localhost:9200'] if ES_HOSTS_ENV not in os.environ else str(os.environ[ES_HOSTS_ENV]).split(',')


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


@app.route('/create/<string:index_name>', methods=['PUT'])
def create(index_name):
    if DocumentIndex.exists(index_name):
        return 'An index with the name %s already exists.' % index_name, 409
    if DocumentIndex.create(index_name):
        return 'Index created', 200
    else:
        return 'Unable to create index', 500


@app.route('/health/<string:name>', methods=['GET'])
def health(name):
    if DocumentIndex.exists(name):
        columns = 'health,status,index,docs.count,store.size'
        es = Elasticsearch(es_hosts)
        health = es.cat.indices(index=name, h=columns).split(' ')
        return render_template('health.html', health=health)
    else:
        return 'Index "%s" does not exist' % name, 404


@app.route('/index/<string:index_name>', methods=['POST'])
def index_documents(index_name):
    if request.is_json:
        try:
            json = request.get_json()
            if DocumentIndex.exists(index_name):
                indexed_documents = DocumentIndex.index(index_name,
                                                        [create_document(index_name,
                                                                         d['title'],
                                                                         d['contents'],
                                                                         d['url']) for d in json])
                return jsonify({'indexed_documents': indexed_documents}), 200
            else:
                return 'Index "%s" does not exist.' % index_name, 404
        except BadRequest:
            return 'An exception was thrown parsing your JSON. Maybe you could try linting it?', 408
    else:
        return 'Request is not JSON. Ensure Content-Type is application/json.', 408


@app.route('/update/<string:index_name>/<uuid:document_id>', methods=['PUT'])
def update_document(index_name, document_id):
    if request.is_json:
        try:
            json = request.get_json()
            if Document.exists(index_name, document_id):
                document = Document.create_document(index_name, document_id, json['title'], json['contents'], json['url'])
                document.save()
                return '', 200
            else:
                return 'Document "%s" does not exist in index "%s".' % (document_id, index_name), 404
        except BadRequest:
            return 'An exception was thrown parsing your JSON. Maybe you could try linting it?', 408
    else:
        return 'Request is not JSON. Ensure Content-Type is application/json.', 408


@app.route('/search/<string:index_name>')
def search(index_name):
    """
    Endepunktet skal være /search/<navn på index> og være tilknyttet HTTP-metoden GET.
    Søkestrengen skal være en query-string.
    :param index_name:  
    :return:
     En liste av dokumenter som matcher søkestrengen. Hvert dokument må være formatert slik:
     {
        "id": "<id>",
        "title": "<tittel>",
        "contents": "<innhold>",
        "url": "<url>",
        "score": "<score>"
     }
    """
    if DocumentIndex.exists(index_name):
        if 'q' in request.args:
            query = urllib.unquote_plus(request.args['q'])
            results = Results.get_results(DocumentIndex.search(index_name, query))
            return jsonify(results), 200
    else:
        return 'Index "%s" does not exist.' % index_name, 404


if __name__ == '__main__':
    app.run()
