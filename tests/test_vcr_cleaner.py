import copy

from vcr_cleaner import CleanYAMLSerializer


def test_with_vcr():

    def clean_robots(request: dict, response: dict):
        response['body']['string'] = \
            response['body']['string'].replace('User-agent', 'CLEAN_ROBOT')

    def clean_all_md(request: dict, response: dict):
        response['body']['string'] = \
            response['body']['string'].replace('User-agent', 'CLEAN_MD')

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner_if_uri_contains(
        clean_robots, uri_contains='/robots.txt'
    )
    serializer.register_cleaner_if_uri_contains(
        clean_all_md, uri_contains='.md'
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


def test_register_uri():

    def undecorated_cleaner(request: dict, response: dict):
        response['body']['string'] = 'TRON'

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner_if_uri_contains(
        undecorated_cleaner,
        uri_contains='/robots.txt'
    )

    tape = {'interactions': [{
        'response': {'body': {"string": 'User-agent'}},
        'request': {'uri': 'helloworld.com/robots.txt'},
    }]}
    expected = copy.deepcopy(tape)
    expected['interactions'][0]['response']['body']['string'] = "TRON"
    result = serializer.deserialize(serializer.serialize(tape))
    assert result == expected


def test_register_cleaner_if_host_startswith():
    def clean_host(request: dict, response: dict):
        response['body']['string'] = 'CLEANED'

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner_if_host_startswith(
        clean_host,
        hostname='example.com'
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


def test_register_cleaner_if_host_startswith_negative():
    """Cleaner should NOT apply if hostname does not match exactly."""
    def clean_host(request: dict, response: dict):
        response['body']['string'] = 'CLEANED'

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner_if_host_startswith(
        clean_host,
        hostname='example.com'
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


def test_register_cleaner_if_path_endswith():
    def clean_path(request: dict, response: dict):
        response['body']['string'] = 'CLEANED'

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner_if_path_endswith(
        clean_path,
        path='robots.txt'
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


def test_register_cleaner_if_path_endswith_negative():
    def clean_path(request: dict, response: dict):
        response['body']['string'] = 'CLEANED'

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner_if_path_endswith(
        clean_path,
        path='robots.txt'
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
