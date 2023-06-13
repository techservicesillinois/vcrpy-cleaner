import os


def clean_env_strings(request: dict, response: dict):
    '''Clean any strings set in the CLEAN_STRING environment variable.

    export CLEAN_STRINGS='my_name,my_email'
    '''
    clean_strings = os.environ.get('CLEAN_STRINGS', "").split(',')
    if clean_strings == ['']:
        return

    # Do not attempt to clean non-string body (i.e. binary auth token)

    if not type(response['body']) == str and not type(response['body']) == dict:
        return

    if 'string' in response['body']:
        body = response['body']['string']
    else:
        body = response['body']

    #if not type(body) == str:
    #    return

    # Clean response body
    for clean_me in clean_strings:
        body = body.replace(clean_me, 'CLEANED')

    if 'string' in response['body']:
        response['body']['string'] = body
    else:
        response['body'] = body
