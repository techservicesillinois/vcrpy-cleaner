import datetime
import gzip
import jwt

CLEANER_SALT = 'salty'
CLEANER_JWT_TOKEN = {'exp': datetime.datetime(2049, 6, 25)}


def clean_token(request: dict, response: dict):
    '''Clean a JWT token.'''

    jwt_token = jwt.encode(CLEANER_JWT_TOKEN, CLEANER_SALT, algorithm='HS256')
    if 'Content-Encoding' in response['headers'].keys() and \
            response['headers']['Content-Encoding'] == ['gzip']:
        token = gzip.compress(bytes(jwt_token, "ascii"))
        response['body']['string'] = token
