import datetime
import gzip
import jwt

from vcr_cleaner.cleaners.jwt_token import CLEANER_JWT_TOKEN, CLEANER_SALT, clean_token


def token_interaction(token: str):
    '''Helper function to build VCR response dictionary'''
    return {
        'request': {},
        'response': {
            'headers': {
                'Content-Encoding': ['gzip'],
            },
            'body': {
                'string': gzip.compress(bytes(
                jwt.encode(token, CLEANER_SALT, algorithm='HS256') , "ascii"))
            }
        }
    }


def test_clean_token():
    token = token_interaction({'exp': datetime.datetime(1970, 1, 1)})
    clean_token(token['request'], token['response'])
    
    expect = token_interaction(CLEANER_JWT_TOKEN)
    assert token == expect
