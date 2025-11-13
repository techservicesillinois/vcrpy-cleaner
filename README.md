# VCR Cleaner

See `def test_if_uri_contains_two_different_scrubs` in `test_filters.py` for usage.

```python
import vcr

from vcr_cleaner import CleanYAMLSerializer
from vcr_cleaner.cleaners.jwt_token import clean_token
from vcr_cleaner.filters import if_uri_contains

yaml_cleaner = CleanYAMLSerializer()

# Register an included function
yaml_cleaner.register_cleaner(if_uri_contains('/api/auth', clean_token))

# Define cleaner functions
def clean_bad_word(request: dict, response: dict):
    response['body']['string'] = response['body']['string'].replace('shid', '')

def clean_long_response(request: dict, response: dict):
    response['body'] = "{'when all your test needs':'is this bit'}"

# Register custom cleaner functions
yaml_cleaner.register_cleaner(if_uri_contains('/api/foulmouth', clean_bad_word))
yaml_cleaner.register_cleaner(if_uri_contains('/api/returns_so_so_many_records',
clean_long_response))

my_vcr = vcr.VCR(
         cassette_library_dir='cassettes',
         record_mode='once',
         filter_headers=[('Authorization', 'Bearer FAKE_TOKEN')],
         match_on=['uri', 'method'],
)
my_vcr.register_serializer("yaml_cleaner", yaml_cleaner)
```
