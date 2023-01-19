import functools

from vcr.serializers import yamlserializer

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

    def register_cleaner(self, function, uri=None):
        if uri:
            @clean_if(uri=uri)
            def decorated(*args, **kwargs):
                function(*args, **kwargs)
        self.cleaners.append(decorated if uri else function)


def clean_if(uri):
    '''Decorates a cleaner method to make it apply only to the given URI'''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, response):
            if request['uri'] != uri:
                return
            func(request, response)
        return wrapper
    return decorator
