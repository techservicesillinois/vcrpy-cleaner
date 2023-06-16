import functools
from typing import TypedDict, Dict, Any, List, Union

from vcr.serializers import yamlserializer
from typing import Callable


class CleanYAMLSerializer:

    def __init__(self):
        self.cleaners = []

    def serialize(self, cassette: dict):
        for interaction in cassette['interactions']:
            for cleaner in self.cleaners:
                cleaner(interaction['request'], interaction['response'])
        return yamlserializer.serialize(cassette)

    @staticmethod
    def deserialize(cassette: str):
        return yamlserializer.deserialize(cassette)

    def register_cleaner(self, function: Callable, uri=None):
        if uri:
            @clean_if(uri=uri)
            def decorated(*args, **kwargs):
                function(*args, **kwargs)
        self.cleaners.append(decorated if uri else function)


def clean_if(uri: str):
    '''Decorates a cleaner method to make it apply only to the given URI'''
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(request: dict, response: dict):
            if request['uri'] != uri:
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
