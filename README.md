See `def test_with_vcr` in `tests/test_vcr_cleaner.py` for usage.

```python
from vcr_cleaner.cleaners.jwt_token import clean_token
from vcr_cleaner import clean_if, CleanYAMLSerializer

yaml_cleaner = CleanYAMLSerializer()

# Register a custom function
@clean_if(uri='https://example.com/api/foulmouth')
def clean_bad_word(request: dict, response: dict):
    response['body']['string'] = response['body']['string'].replace('shid', '')

yaml_cleaner.register_cleaner(clean_bad_word)

# Register an included function
yaml_cleaner.register_cleaner(clean_token, uri='https://example.com/api/auth')

my_vcr = vcr.VCR(
         cassette_library_dir='cassettes',
         record_mode='once',
         filter_headers=[('Authorization', 'Bearer FAKE_TOKEN')],
         match_on=['uri', 'method'],
)
my_vcr.register_serializer("yaml_cleaner", yaml_cleaner)
```