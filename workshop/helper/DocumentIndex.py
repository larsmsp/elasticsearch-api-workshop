from elasticsearch_dsl import Index, analyzer

import workshop.model.Document


def create(name, analyzer_name='norwegian'):
    index = Index(name)
    index.settings(
        number_of_shards=2,
        number_of_replicas=1
    )
    index.doc_type(workshop.model.Document)
    index.analyzer(analyzer(analyzer_name))
    index.delete(ignore=404)
    index.create()
    return exists(name)


def exists(name):
    return Index(name).exists()
