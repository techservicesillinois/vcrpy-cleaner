import os

def clean_env_strings(request: dict, response: dict):
    if request:
        clean_env_helper(request)
    if response:
        clean_env_helper(response)


def clean_env_helper(dirty: dict):
    '''Clean any strings set in the CLEAN_STRING environment variable.

    export CLEAN_STRINGS='my_name,my_email'
    '''
    clean_strings = os.environ.get('CLEAN_STRINGS', "").split(',')
    if clean_strings == ['']:
        return

    # Only string body and a dict body with a key named 'string' are currently supported
    if not type(dirty['body']) == str and not type(dirty['body']) == dict:
        return

    if 'string' in dirty['body']:
        body = dirty['body']['string']
    else:
        body = dirty['body']

    # Do not attempt to clean non-string body (i.e. binary auth token)
    if not type(body) == str:
        return

    # Clean response body
    for clean_me in clean_strings:
        body = body.replace(clean_me, 'CLEANED')

    if 'string' in dirty['body']:
        dirty['body']['string'] = body
    else:
        dirty['body'] = body
