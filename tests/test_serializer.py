
# Python imports
import datetime
import gzip
import os

# Library imports
import jwt
import pytest
import vcr

# VCRpy Cleaner imports
from vcrpy_cleaner import CleanYAMLSerializer

# To record, `export VCR_RECORD=True`
VCR_RECORD = "VCR_RECORD" in os.environ

CLEANER_SALT = 'salty'
CLEANER_JWT_TOKEN = {'exp': datetime.datetime(2049, 6, 25)}


def token_response(raw_token: str):
    '''Helper function to build VCR response dictionary'''
    return {
        'response': {
            'headers': {
                'Content-Encoding': ['gzip'],
            },
            'body': {
                'string': gzip.compress(bytes(
                jwt.encode(raw_token, CLEANER_SALT, algorithm='HS256') , "ascii"))
            }
        }
    }


def clean_token(interaction: dict):
    '''Just an example function we can test with our tool.'''
    # if interaction['request']['uri'] != uri:
    #    return

    token = jwt.encode(CLEANER_JWT_TOKEN, CLEANER_SALT, algorithm='HS256')
    response = interaction['response']
    if 'Content-Encoding' in response['headers'].keys() and \
            response['headers']['Content-Encoding'] == ['gzip']:
        token = gzip.compress(bytes(token, "ascii"))
    response['body']['string'] = token


def test_clean_token():
    target = {'exp': datetime.datetime(1970, 1, 1)}
    expected = CLEANER_JWT_TOKEN
    token = token_response(target)
    clean_token(token)
    
    assert token['response']['body']['string'] == token_response(expected)['response']['body']['string']


# TODO: Test with serializer
def test_with_vcr():

    # Assemble
    serializer = CleanYAMLSerializer()
    serializer.register_cleaner(clean_token, uri='/api/foo')

    my_vcr = vcr.VCR(
        cassette_library_dir='cassettes',
        record_mode='once' if VCR_RECORD else 'none',
        match_on=['uri', 'method'],
    )
    my_vcr.register_serializer("cleanyaml", serializer)

    # Act
    # TODO: Serialize something with a token to clean, using vcr

    # Assert
    # TODO: Verify the VCR serialized YAML contains CLEANER_JWT_TOKEN
