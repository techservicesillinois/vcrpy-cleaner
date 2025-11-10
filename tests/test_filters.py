import copy

from vcr_cleaner import CleanYAMLSerializer
from vcr_cleaner.filters import (
    if_uri_contains,
    if_uri_endswith,
    if_uri_startswith,
)


def test_if_uri_contains_two_different_scrubs():
    """ Test if two different filters conflict. """
    def clean_robots(request: dict, response: dict):
        response['body']['string'] = \
            response['body']['string'].replace('User-agent', 'CLEAN_ROBOT')

    def clean_all_md(request: dict, response: dict):
        response['body']['string'] = \
            response['body']['string'].replace('User-agent', 'CLEAN_MD')

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner(
        if_uri_contains('/robots.txt', clean_robots)
    )
    serializer.register_cleaner(
        if_uri_contains('.md', clean_all_md)
    )
    tape = {'interactions': [
        {'response': {'body': {"string": 'User-agent'}},
         'request': {'uri': 'helloworld.com/robots.txt'}, },
        {'response': {'body': {"string": 'User-agent'}},
         'request': {'uri': 'helloworld.com/file.md'}, }
    ]}
    expected = copy.deepcopy(tape)
    expected['interactions'][0]['response']['body']['string'] = "CLEAN_ROBOT"
    expected['interactions'][1]['response']['body']['string'] = "CLEAN_MD"
    result = serializer.deserialize(serializer.serialize(tape))
    assert result == expected


def test_if_uri_contains_no_scrub():

    def clean_body(request: dict, response: dict):
        response['body']['string'] = 'TRON'

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner(
        if_uri_contains('/robots.txt', clean_body)
    )

    tape = {'interactions': [{
        'response': {'body': {"string": 'User-agent'}},
        'request': {'uri': 'helloworld.com/robots.txt'},
    }]}
    expected = copy.deepcopy(tape)
    expected['interactions'][0]['response']['body']['string'] = "TRON"
    result = serializer.deserialize(serializer.serialize(tape))
    assert result == expected


def test_if_uri_startswith():

    def clean_body(request: dict, response: dict):
        response['body']['string'] = 'CLEANED'

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner(
        if_uri_startswith('example.com', clean_body)
    )

    tape = {'interactions': [
        {'response': {'body': {"string": 'User-agent'}},
            'request': {'uri': 'example.com/robots.txt'}},
        {'response': {'body': {"string": 'User-agent'}},
            'request': {'uri': 'https://example.com/api/v1/users'}},
        {'response': {'body': {"string": 'User-agent'}},
            'request': {'uri': 'http://example.com/robots.txt'}},
    ]}
    expected = copy.deepcopy(tape)
    for interaction in expected['interactions']:
        interaction['response']['body']['string'] = 'CLEANED'
    result = serializer.deserialize(serializer.serialize(tape))
    assert result == expected


def test_if_uri_startswith_negative():
    """Cleaner should NOT apply if hostname does not match exactly."""

    def clean_body(request: dict, response: dict):
        response['body']['string'] = 'CLEANED'

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner(
        if_uri_startswith('example.com', clean_body)
    )

    tape = {'interactions': [
        {'response': {'body': {"string": 'User-agent'}},
            'request': {'uri': 'notexample.com/robots.txt'}},
        {'response': {'body': {"string": 'User-agent'}},
            'request': {'uri': 'sample.com/robots.txt'}},
        {'response': {'body': {"string": 'User-agent'}},
            'request': {'uri': 'http://fooexample.com/robots.txt'}},
        {'response': {'body': {"string": 'User-agent'}},
            'request': {'uri': 'https://bar.com/api/v1/users'}},
    ]}
    expected = copy.deepcopy(tape)
    result = serializer.deserialize(serializer.serialize(tape))
    assert result == expected


def test_if_uri_endswith():
    def clean_body(request: dict, response: dict):
        response['body']['string'] = 'CLEANED'

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner(
        if_uri_endswith('robots.txt', clean_body)
    )

    tape = {'interactions': [
        {'response': {'body': {"string": 'User-agent'}},
         'request': {'uri': 'example.com/robots.txt'}},
        {'response': {'body': {"string": 'User-agent'}},
         'request': {'uri': 'http://other.com/api/robots.txt'}},
        {'response': {'body': {"string": 'User-agent'}},
         'request': {'uri': 'https://foo.com/robots.txt'}},
    ]}
    expected = copy.deepcopy(tape)
    for interaction in expected['interactions']:
        interaction['response']['body']['string'] = 'CLEANED'
    result = serializer.deserialize(serializer.serialize(tape))
    assert result == expected


def test_if_uri_endswith_negative():
    def clean_body(request: dict, response: dict):
        response['body']['string'] = 'CLEANED'

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner(
        if_uri_endswith('robots.txt', clean_body)
    )

    tape = {'interactions': [
        {'response': {'body': {"string": 'User-agent'}},
         'request': {'uri': 'example.com/other.txt'}},
        {'response': {'body': {"string": 'User-agent'}},
         'request': {'uri': 'http://other.com/api/other.txt'}},
        {'response': {'body': {"string": 'User-agent'}},
         'request': {'uri': 'https://foo.com/other.txt'}},
    ]}
    expected = copy.deepcopy(tape)
    result = serializer.deserialize(serializer.serialize(tape))
    assert result == expected
