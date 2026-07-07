import datetime
import gzip
import jwt


CLEANER_SALT = 'PleaseChangeThisSaltToSomethingElse'
CLEANER_JWT_TOKEN = {'exp': datetime.datetime(2049, 6, 25)}


def clean_token(request: dict, response: dict, algorithm='HS256'):
    '''Clean a JWT token.'''

    jwt_token = jwt.encode(
        CLEANER_JWT_TOKEN, CLEANER_SALT, algorithm)
    if 'Content-Encoding' in response['headers'].keys() and \
            response['headers']['Content-Encoding'] == ['gzip']:
        response['body']['string'] = jwt_token
