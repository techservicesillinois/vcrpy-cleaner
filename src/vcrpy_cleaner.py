

class CleanYAMLSerializer:
    '''VCR.py YAML serializer that applies data cleaners as it serializes.
    
    See src/cleaners for included cleaner functions.
    '''
    def __init__(self):
        self._cleaners = []

    def register_cleaner(self, cleaner_function, uri):
        self._cleaners.append((cleaner_function, uri))

    def serialize(self, cassette: dict):
        for interaction in cassette['interactions']:
            for clean_yaml, match_uri in self._cleaners:
                if interaction['request']['uri'] == uri:
                    clean_yaml(interaction)
        return yamlserializer.serialize(cassette)

    def deserialize(self, cassette: str):
        return yamlserializer.deserialize(cassette)