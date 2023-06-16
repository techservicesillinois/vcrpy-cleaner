import copy

from vcr_cleaner import clean_if, CleanYAMLSerializer


def test_with_vcr():
    @clean_if(uri='helloworld.com/robots.txt')
    def clean_robots(request: dict, response: dict):
        response['body']['string'] = \
            response['body']['string'].replace('User-agent', 'TRON')

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner(clean_robots)
    tape = {'interactions': [{
        'response': {'body': {"string": 'User-agent'}},
        'request': {'uri': 'helloworld.com/robots.txt'},
    }]}
    expected = copy.deepcopy(tape)
    expected['interactions'][0]['response']['body']['string'] = "TRON"
    result = serializer.deserialize(serializer.serialize(tape))
    assert result == expected


def test_register_uri():

    def undecorated_cleaner(request: dict, response: dict):
        response['body']['string'] = 'TRON'

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner(undecorated_cleaner,
                                uri='helloworld.com/robots.txt')

    tape = {'interactions': [{
        'response': {'body': {"string": 'User-agent'}},
        'request': {'uri': 'helloworld.com/robots.txt'},
    }]}
    expected = copy.deepcopy(tape)
    expected['interactions'][0]['response']['body']['string'] = "TRON"
    result = serializer.deserialize(serializer.serialize(tape))
    assert result == expected
