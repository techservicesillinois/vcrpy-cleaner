import datetime
import gzip
import jwt

from cleaners.jwt_token import CLEANER_JWT_TOKEN, CLEANER_SALT, clean_token


def token_response(token: str):
    '''Helper function to build VCR response dictionary'''
    return {
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
    target = {'exp': datetime.datetime(1970, 1, 1)}
    expected = CLEANER_JWT_TOKEN
    token = token_response(target)
    clean_token(token)
    
    assert token['response']['body']['string'] == \
        token_response(expected)['response']['body']['string']
