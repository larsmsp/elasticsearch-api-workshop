import sys

from elasticsearch_dsl import Index, analyzer, Search
from os.path import join, abspath, dirname
from elasticsearch_dsl import Index, analyzer

sys.path.append(join(dirname(abspath(__file__)), '../..'))

from workshop.model.Document import Document


def create(name, analyzer_name='norwegian'):
    index = Index(name)
    index.settings(
        number_of_shards=2,
        number_of_replicas=0
    )
    index.doc_type(Document)
    index.analyzer(analyzer(analyzer_name))
    index.delete(ignore=404)
    index.create()
    return exists(name)


def exists(name):
    return Index(name).exists()
