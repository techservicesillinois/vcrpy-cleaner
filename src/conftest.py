import logging
import os

# import pytest
import vcr

from vcr.serializers import yamlserializer

# CASSETTE_USERNAME = "FAKE_USERNAME"
# CASSETTE_PASSWORD = "FAKE_PASSWORD"
# CASSETTE_ENDPOINT = "cybersecurity.illinois.edu/robots.txt"

# To record, `export VCR_RECORD=True`
# VCR_RECORD = "VCR_RECORD" in os.environ


class CleanYAMLSerializer:

    def __init__(self):
        self.cleaners = []

    @staticmethod
    def serialize(cassette: dict):
        for interaction in cassette['interactions']:
            for cleaner in self.cleaners:
                cleaner(interaction)
        return yamlserializer.serialize(cassette)

    @staticmethod
    def deserialize(cassette: str):
        return yamlserializer.deserialize(cassette)

    def register_cleaner(function):
        self.cleaners.append(function)


def cleaner(uri):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return
        return wrapper
    return decorator


@cleaner(uri="ba")
def custum_foo(interaction):
   pass

# Can not generlize as a fixture due to AppConnector dependency
#@pytest.fixture
#def connector(monkeypatch) -> AppConnector:
#    conn = AppConnector()
#    if not VCR_RECORD:  # Always use cassette values when using cassette
#        conn.config = {
#            "username": CASSETTE_USERNAME,
#            "password": CASSETTE_PASSWORD,
#            "endpoint": CASSETTE_ENDPOINT,
#        }
#    else:  # User environment values
#        env_keys = ['username', 'password', 'endpoint']
#
#        for key in env_keys:
#            env_key = f"APP_{key.upper()}"
#            conn.config[key] = os.environ.get(env_key, None)
#            if not conn.config[key]:
#                raise ValueError(f'{env_key} unset or empty with record mode')
#
#    conn.logger.setLevel(logging.INFO)
#    return conn


# TODO: Do we want this here or in a seperate pytest dependent library?
#@pytest.fixture
#def cassette(request) -> vcr.cassette.Cassette:
#    my_vcr = vcr.VCR(
#        cassette_library_dir='cassettes',
#        record_mode='once' if VCR_RECORD else 'none',
#        # TODO: Uncomment with remove_creds from shared repo
#        # before_record_request=remove_creds,
#        filter_headers=[('Authorization', 'Bearer FAKE_TOKEN')],
#        match_on=['uri', 'method'],
#    )
####### Pseudo-code
#    serializer = CleanYAMLSerializer()
#    serializer.register_cleaner(imported_fun1)
#    serializer.register_cleaner(builtin_fun2)
#    my_vcr.register_serializer("cleanyaml", serializer)
######
#    my_vcr.register_serializer("cleanyaml", CleanYAMLSerializer)
#
#    with my_vcr.use_cassette(f'{request.function.__name__}.yaml',
#                             serializer="cleanyaml") as tape:
#        yield tape
#        if my_vcr.record_mode == 'none':  # Tests only valid when not recording
#            assert tape.all_played, \
#                f"Only played back {len(tape.responses)} responses"
