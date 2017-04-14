from datetime import datetime
from elasticsearch_dsl import DocType, String, Date


class Document(DocType):

    title = String()
    contents = String()
    url = String()
    created_at = Date()

    def __init__(self, _index, _document_id, **kwargs):
        super(Document, self).__init__(meta={'id': _document_id, 'index': _index}, **kwargs)
        self.created_at = datetime.now()
