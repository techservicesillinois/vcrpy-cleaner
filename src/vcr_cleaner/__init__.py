import functools
from typing import TypedDict, Dict, Any, List, Union

from vcr.serializers import yamlserializer
from typing import Callable


class CleanYAMLSerializer:

    def __init__(self):
        self.cleaners = []

    def serialize(self, cassette: dict):
        '''
        Applies our cleaners while VCR.py serializes web traffic into a
        cassette.
        '''
        for interaction in cassette['interactions']:
            for cleaner in self.cleaners:
                cleaner(interaction['request'], interaction['response'])
        return yamlserializer.serialize(cassette)

    @staticmethod
    def deserialize(cassette: str):
        return yamlserializer.deserialize(cassette)

    def register_cleaner(self, function: Callable):
        '''Apply this cleaner function to all cassette contents.'''
        self.cleaners.append(function)

    def register_cleaner_if_host_startswith(
        self, function: Callable, hostname: str
    ):
        '''
        Apply registered cleaner only if URI hostname before the first `/`
        matches the given text.

        'example.com' will match 'https://example.com/robots.txt'
        'example.com' will match 'https://example.com/api/v1/users'
        '''
        @_apply_if_uri_startswith(uri_starts=hostname)
        def decorated(*args, **kwargs):
            function(*args, **kwargs)
        self.register_cleaner(decorated)

    def register_cleaner_if_path_endswith(self, function: Callable, path: str):
        '''
        Apply registered cleaner only if URI path after the first `/`
        matches the given text.
        '''
        @_apply_if_uri_endswith(uri_ends=path)
        def decorated(*args, **kwargs):
            function(*args, **kwargs)
        self.register_cleaner(decorated)

    def register_cleaner_if_uri_contains(
        self,
        function: Callable,
        uri_contains: str
    ):
        '''Apply registered cleaner only if URI contains the given text.'''

        @_apply_if_uri_contains(uri_contains=uri_contains)
        def decorated(*args, **kwargs):
            function(*args, **kwargs)
        self.register_cleaner(decorated)


def _apply_if_uri_contains(uri_contains: str):
    '''Decorates a cleaner method to make it apply to any cassette interactions
    where the URI contains the text passed to `uri_contains`.

    Typically applied by the matching `register_cleaner_if...` function above.
    '''

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(request: dict, response: dict):
            if uri_contains not in request['uri']:
                return
            func(request, response)
        return wrapper
    return decorator


def _apply_if_uri_startswith(uri_starts: str):
    '''Decorates a cleaner method to make it apply to any cassette interactions
    where the URI starts with the text passed to `uri_starts`.

    Typically applied by the matching `register_cleaner_if...` function above.

    'example.com' will match 'example.com/robots.txt'
    'example.com' will match 'example.com/api/v1/users'
    '''

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(request: dict, response: dict):
            hostname = (
                request['uri']
                .lower()
                .lstrip('https://')
                .lstrip('http://')
            )
            if not hostname.startswith(uri_starts):
                return
            func(request, response)
        return wrapper
    return decorator


def _apply_if_uri_endswith(uri_ends: str):
    '''Decorates a cleaner method to make it apply to any cassette interactions
    where the URI ends with the text passed to `uri_ends`.

    Typically applied by the matching `register_cleaner_if...` function above.

    'robots.txt' will match 'example.com/robots.txt'
    'api/v1/users' will match 'example.com/api/v1/users'
    '''

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(request: dict, response: dict):
            if not request['uri'].endswith(uri_ends):
                return
            func(request, response)
        return wrapper
    return decorator


class StringBodyResponse(TypedDict):
    '''MyPy type for a web response whose body is a string.'''
    headers: dict[str, List[str]]
    body: str


class StringBodyRequest(TypedDict):
    '''MyPy type for a web request whose body is a string.'''
    headers: dict[str, List[str]]
    body: str


class StringBodyInteraction(TypedDict):
    '''MyPy type for a web interaction whose response body is a string.'''
    request: Dict[Any, Any]
    response: StringBodyResponse


class DictBodyResponse(TypedDict):
    '''MyPy type for a web response whose body is a dictionary.'''
    headers: dict[str, List[str]]
    body: dict[str, Union[bytes, str]]


class BytesBodyResponse(TypedDict):
    '''MyPy type for a web response whose body is a dictionary.'''
    headers: dict[str, List[str]]
    body: bytes


class DictBodyInteraction(TypedDict):
    '''MyPy type for a web interaction whose response body is a dictionary.'''
    request: Dict[Any, Any]
    response: DictBodyResponse


class JWTTokenResponse(TypedDict):
    '''MyPy type for a web response whose body is a dictionary
      containing a JWT token.'''
    headers: dict[str, List[str]]
    body: dict[str, bytes]


class JWTTokenInteraction(TypedDict):
    '''MyPy type for a web interaction whose response body is a dictionary
      containing a JWT token.'''
    request: Dict[Any, Any]
    response: JWTTokenResponse


Response = Union[
    BytesBodyResponse,
    DictBodyResponse,
    StringBodyResponse,
]
