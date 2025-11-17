from vcr_cleaner.cleaners.uri import (
    clean_domains,
    clean_uri,
)


def test_simple_clean_uri():
    '''Test simple usage of clean_uri.'''
    request = {
        'uri': 'https://example.com'
    }

    cleaner = clean_uri('example', 'foo')
    assert cleaner(request, None)['uri'] == 'https://foo.com'
    assert cleaner.__name__ == "clean_uri"
    assert str(cleaner.__doc__) != 'None'
    assert 'example' in str(cleaner.__doc__)
    assert 'foo' in str(cleaner.__doc__)


def test_clean_domain():
    request = {
        'sub-domain': 'https://foo.illinois.edu',
        'sub-sub-domain': 'https://foo.bar.illinois.edu',
        'uri': 'https://illinois.edu',
        'insecure': 'http://illinois.edu',
        'essay': 'Lorum ipsum https://illinois.edu, and so on...',
    }
    response = request.copy()

    cleaner = clean_domains('illinois.edu')
    cleaner(request, response)

    assert str(cleaner.__doc__) != 'None'

    for key in ['uri', 'sub-domain', 'sub-sub-domain']:
        assert request[key] == 'https://cleaned.example.edu'

    assert request['insecure'] == 'http://cleaned.example.edu'
    assert 'illinois.edu' not in request['essay']

    assert request == response
