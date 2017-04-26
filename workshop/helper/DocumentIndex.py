from elasticsearch.helpers import bulk
from elasticsearch_dsl import Index, analyzer, Search
from elasticsearch_dsl.connections import connections

from model import Document


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


def index(name, documents):
    conn = connections.get_connection()
    actions = ({
                   '_op_type': 'index',
                   '_index': name,
                   '_type': 'document',
                   '_source': d
               } for d in documents)
    return bulk(conn, actions)[0]


def search(name, query):
    s = Search(index=name)\
        .highlight_options(require_field_match=False,
                           fragment_size=250,
                           pre_tags=['**'],
                           post_tags=['**'])\
        .highlight('contents')\
        .query('query_string', query=query)
    return s.execute()

