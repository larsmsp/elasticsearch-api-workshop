import uuid

from datetime import datetime
from elasticsearch_dsl import DocType, String, Date
from elasticsearch import NotFoundError


class Document(DocType):

    title = String()
    contents = String()
    url = String()
    created_at = Date()

    def __init__(self, document_id, index, **kwargs):
        super(Document, self).__init__(meta={'id': document_id, 'index': index}, **kwargs)
        self.created_at = datetime.now()


def create_document(index, id, title, contents, url):
    document = Document(id, index)
    document.title = title
    document.contents = contents
    document.url = url
    return document


def exists(document_id, index):
    try:
        Document.get(id=document_id, index=index)
        return True
    except NotFoundError:
        return False

