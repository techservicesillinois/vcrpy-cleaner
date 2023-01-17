
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

# TODO: Add unit tests. 

# TODO: Think about how to get rid of need 
# to export VCR_RECORD and deleting the YAML
def test_with_vcr(cassette):

    # Assemble
    @cleaner(uri=f'{CASSETTE_ENDPOINT}/robots.txt')
    def clean_robots(interaction: dict):
        '''Trivial cleaner function for testing.

        Replaces 'User-agent' in any robots.txt file response.
        '''
        response = interaction['response']
        response['body']['string'] = \
            response['body']['string'].replace('User-agent', 'TRON')

    cassette._serializer.register_cleaner(clean_robots)

    # Act
    response = requests.get(f'{CASSETTE_ENDPOINT}/robots.txt')

    # Assert
    assert response.status_code == 200
    # TODO: Open and examine the generated YAML in the cassette.
    with open(cassette._path, 'r') as cassette_file:
        cassette_content = cassette_file.read()
        assert 'User-agent' not in cassette_content

    # assert 'TRON' in cassette.responses[0]['body']['string']
