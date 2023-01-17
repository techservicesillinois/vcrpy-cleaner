import datetime
import gzip
import jwt

CLEANER_SALT = 'salty'
CLEANER_JWT_TOKEN = {'exp': datetime.datetime(2049, 6, 25)}


def clean_token(interaction: dict):
    '''Clean a JWT token.'''

    token = jwt.encode(CLEANER_JWT_TOKEN, CLEANER_SALT, algorithm='HS256')
    response = interaction['response']
    if 'Content-Encoding' in response['headers'].keys() and \
            response['headers']['Content-Encoding'] == ['gzip']:
        token = gzip.compress(bytes(token, "ascii"))
    response['body']['string'] = token