
# Python imports
import datetime
import gzip
import os

# Library imports
import jwt
import pytest
import requests
import vcr

# VCRpy Cleaner imports
from vcr_cleaner import CleanYAMLSerializer, cleaner, cassette
from cleaners.jwt_token import clean_token

# To record, `export VCR_RECORD=True`

CASSETTE_ENDPOINT = 'https://cybersecurity.illinois.edu'

def clean_robots():
    '''Trivial cleaner function for testing.

    Replaces 'User-agent' in any robots.txt file response.
    '''


# TODO: Test with serializer
@cleaner(uri=f'{CASSETTE_ENDPOINT}/robots.txt')
def test_with_vcr(cassette):

    # Assemble

    # Act
    response = requests.get(f'{CASSETTE_ENDPOINT}/robots.txt')
    assert response.status_code == 200
    # TODO: Open and examine the generated YAML in the cassette.
