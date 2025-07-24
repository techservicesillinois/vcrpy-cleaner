# VCR Cleaner

See `def test_with_vcr` in `tests/test_vcr_cleaner.py` for usage.

```python
from vcr_cleaner.cleaners.jwt_token import clean_token
from vcr_cleaner import CleanYAMLSerializer

yaml_cleaner = CleanYAMLSerializer()

# Register an included function
yaml_cleaner.register_cleaner_if_uri_contains(clean_token, '/api/auth')

# Define cleaner functions
def clean_bad_word(request: dict, response: dict):
    response['body']['string'] = response['body']['string'].replace('shid', '')

def clean_long_response(request: dict, response: dict):
    response['body'] = "{'when all your test needs':'is this bit'}"

# Register custom cleaner functions
yaml_cleaner.register_cleaner_if_uri_contains(clean_bad_word, '/api/foulmouth')
yaml_cleaner.register_cleaner_if_uri_contains(clean_long_response, '/api/returns_so_so_many_records')

my_vcr = vcr.VCR(
         cassette_library_dir='cassettes',
         record_mode='once',
         filter_headers=[('Authorization', 'Bearer FAKE_TOKEN')],
         match_on=['uri', 'method'],
)
my_vcr.register_serializer("yaml_cleaner", yaml_cleaner)
```
