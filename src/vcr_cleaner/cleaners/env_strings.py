import os
from typing import overload

from vcr_cleaner import (
    StringBodyResponse,
    StringBodyRequest,
    DictBodyResponse,
    BytesBodyResponse,
    Response,
)


def clean_env_strings(request: StringBodyRequest, response: Response):
    if request:
        clean_env_helper(request)
    if response:
        clean_env_helper(response)


@overload
def clean_env_helper(dirty: BytesBodyResponse) -> None:
    ...


@overload
def clean_env_helper(dirty: StringBodyResponse) -> None:
    ...


@overload
def clean_env_helper(dirty: DictBodyResponse) -> None:
    ...


def clean_env_helper(dirty):
    '''Clean any strings set in the CLEAN_STRING environment variable.

    export CLEAN_STRINGS='my_name,my_email'
    '''
    clean_strings = os.environ.get('CLEAN_STRINGS', "").split(',')
    if clean_strings == ['']:
        return

    # Only string body and a dict body with a key named 'string'
    # are currently supported
    if type(dirty['body']) is not str and type(dirty['body']) is not dict:
        return

    if 'string' in dirty['body']:
        body = dirty['body']['string']
    else:
        body = dirty['body']

    # Do not attempt to clean non-string body (i.e. binary auth token)
    if type(body) is not str:
        return

    # Clean response body
    for clean_me in clean_strings:
        if clean_me.strip() != '':
            body = body.replace(clean_me, 'CLEANED')

    if 'string' in dirty['body']:
        dirty['body']['string'] = body
    else:
        dirty['body'] = body


def simple_clean_env_string(dirty):
    '''Clean any strings set in the CLEAN_STRING environment variable.
    export CLEAN_STRINGS='my_name,my_email'
    '''
    clean_strings = os.environ.get('CLEAN_STRINGS', "").split(',')
    for clean_me in clean_strings:
        if clean_me.strip() != '':
            dirty = dirty.replace(clean_me, 'CLEANED')

    return dirty
