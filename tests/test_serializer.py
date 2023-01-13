# from pyvcr_cleaner import CleanYAMLSerializer
import datetime
import jwt
import gzip
import pytest


def token_response(raw_token: str):
    '''Helper function to build VCR response dictionary'''
    return {
        'response': {
            'headers': {
                'Content-Encoding': ['gzip'],
            },
            'body': {
                'string': gzip.compress(bytes(
                jwt.encode(raw_token, 'salty', algorithm='HS256') , "ascii"))
            }
        }
    }


def clean_token(interaction: dict):
    '''Just an example function we can test with our tool.'''
    # if interaction['request']['uri'] != uri:
    #    return

    token = jwt.encode(
        {'exp': datetime.datetime(2049, 6, 25)}, 'arenofun', algorithm='HS256')
    response = interaction['response']
    if 'Content-Encoding' in response['headers'].keys() and \
            response['headers']['Content-Encoding'] == ['gzip']:
        token = gzip.compress(bytes(token, "ascii"))
    response['body']['string'] = token


def test_clean_token():
    target = {'exp': datetime.datetime(1970, 1, 1)}
    expected = {'exp': datetime.datetime(2049, 6, 25)}
    token = token_response(target)
    clean_token(token)
    
    assert token['response']['body']['string'] == token_response(expected)['response']['body']['string']


# TODO: Test with serializer
#def test_with_vcr():
#
#    serializer = CleanYAMLSerializer()
#    serializer.register_cleaner(clean_token, uri='/api/foo')
#    my_vcr.register_serializer("cleanyaml", serializer)
