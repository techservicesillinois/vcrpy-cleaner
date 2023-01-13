
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

@cleaner(uri=f'{CASSETTE_ENDPOINT}/robots.txt')
def clean_robots(interaction: dict):
    '''Trivial cleaner function for testing.

    Replaces 'User-agent' in any robots.txt file response.
    '''
    response = interaction['response']
    response['body']['string'].replace('User-agent', 'TRON')


# TODO: Test with serializer
def test_with_vcr(cassette):

    # Assemble
    def get_ye_robots():
        return requests.get(f'{CASSETTE_ENDPOINT}/robots.txt')

    # Act
    response = get_ye_robots()

    # Assert
    assert response.status_code == 200
    # TODO: Open and examine the generated YAML in the cassette.
    assert 'TRON' in cassette.responses[0]['body']['string']
