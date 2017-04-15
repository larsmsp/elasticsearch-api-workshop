def get_results(response):
    results = {
        'index': '',
        'results': [],
        'total': 0
    }
    for hit in response:
        document = {
            'id': hit.meta.id,
            'title': hit.title,
            'contents': hit.contents,
            'url': hit.url,
            'score': hit.meta.score,
            'highlight': list(hit.meta.highlight['contents'])
        }
        results['index'] = hit.meta.index
        results['results'].append(document)
        results['total'] += 1
    return results
