import requests

from vcr_cleaner import cleaner, CleanYAMLSerializer


def test_with_vcr():
    @cleaner(uri=f'helloworld.com/robots.txt')
    def clean_robots(interaction: dict):
        '''Trivial cleaner function for testing.

        Replaces 'User-agent' in any robots.txt file response.
        '''
        response = interaction['response']
        response['body']['string'] = \
            response['body']['string'].replace('User-agent', 'TRON')

    serializer = CleanYAMLSerializer()
    serializer.register_cleaner(clean_robots)
    tape = {'interactions': [{
        'response': {'body': {"string": 'User-agent'}},
        'request': {'uri': 'helloworld.com/robots.txt'},
    }]}
    expected = tape.copy()
    expected['interactions'][0]['response']['body']['string'] = "TRON"
    result = serializer.deserialize(serializer.serialize(tape))
    assert result == expected
