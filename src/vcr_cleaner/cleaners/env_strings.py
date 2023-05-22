import os


def clean_env_strings(request: dict, response: dict):
    '''Clean any strings set in the CLEAN_STRING environment variable.

    export CLEAN_STRINGS='my_name,my_email'
    '''
    clean_strings = os.environ.get('CLEAN_STRINGS', "").split(',')

    # Do not attempt to clean a binary blog response body (i.e. auth token)
    if 'bytes' in str(type(response['body']['string'])):
        return

    # Clean response body
    body = response['body']['string']
    for clean_me in clean_strings:
        body = body.replace(clean_me, 'CLEANED')
    response['body']['string'] = body