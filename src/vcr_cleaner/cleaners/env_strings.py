import os


def clean_env_strings(request: dict, response: dict):
    '''Clean any strings set in the CLEAN_STRING environment variable.

    export CLEAN_STRINGS='my_name,my_email'
    '''
    clean_strings = os.environ.get('CLEAN_STRINGS', "").split(',')

    # Do not attempt to clean non-string body (i.e. binary auth token)
    body = response['body']['string']
    if not type(body) == str:
        return

    # Clean response body
    for clean_me in clean_strings:
        body = body.replace(clean_me, 'CLEANED')
    response['body']['string'] = body