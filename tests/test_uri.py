from vcr_cleaner.cleaners.uri import clean_uri


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
