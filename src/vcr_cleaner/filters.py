from typing import Callable


def if_uri_contains(substring: str, func: Callable):
    '''Limit the cleaner `func` to apply to only cassette interactions
    where the URI contains `substring`. '''
    def wrapper(request: dict, response: dict):
        if substring in request['uri']:
            func(request, response)
    return wrapper


def if_uri_endswith(suffix: str, func: Callable):
    '''Limit the cleaner `func` to apply to only cassette interactions
    where the URI ends with the `suffix`.'''
    def wrapper(request: dict, response: dict):
        if request['uri'].endswith(suffix):
            func(request, response)
    return wrapper


def if_uri_startswith(prefix: str, func: Callable):
    '''Limit the cleaner `func` to apply to only cassette interactions
    where the URI starts with the `prefix`. '''
    def wrapper(request: dict, response: dict):
        hostname = request['uri'].lower()
        if hostname.startswith('https://'):
            hostname = hostname[8:]
        elif hostname.startswith('http://'):
            hostname = hostname[7:]

        if hostname.startswith(prefix):
            func(request, response)
    return wrapper
