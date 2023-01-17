import os
import pytest
import vcr

from .vcr_cleaner import CleanYAMLSerializer

# To record, `export VCR_RECORD=True`
VCR_RECORD = "VCR_RECORD" in os.environ

# CASSETTE_USERNAME = "FAKE_USERNAME"
# CASSETTE_PASSWORD = "FAKE_PASSWORD"
# CASSETTE_ENDPOINT = "cybersecurity.illinois.edu/robots.txt"

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

@pytest.fixture
def cassette(request) -> vcr.cassette.Cassette:
    my_vcr = vcr.VCR(
        cassette_library_dir='cassettes',
        record_mode='once' if VCR_RECORD else 'none',
        # TODO: Uncomment with remove_creds from shared repo
        # before_record_request=remove_creds,
        filter_headers=[('Authorization', 'Bearer FAKE_TOKEN')],
        match_on=['uri', 'method'],
    )
####### Pseudo-code
    serializer = CleanYAMLSerializer()
    # TODO: Apply all cleaners from @cleaner decorator
    # serializer.register_cleaner(imported_fun1)
    # serializer.register_cleaner(builtin_fun2)
    my_vcr.register_serializer("cleanyaml", serializer)
######
    # my_vcr.register_serializer("cleanyaml", CleanYAMLSerializer)

    with my_vcr.use_cassette(f'{request.function.__name__}.yaml',
                             serializer="cleanyaml") as tape:
        yield tape
        if my_vcr.record_mode == 'none':  # Tests only valid when not recording
            assert tape.all_played, \
                f"Only played back {len(tape.responses)} responses"
