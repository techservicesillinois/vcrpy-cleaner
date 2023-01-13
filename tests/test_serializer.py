
# Python imports
import datetime
import gzip
import os

# Library imports
import jwt
import pytest
import vcr

# VCRpy Cleaner imports
from vcrpy_cleaner import CleanYAMLSerializer
from cleaners.jwt_token import clean_token

# To record, `export VCR_RECORD=True`
VCR_RECORD = "VCR_RECORD" in os.environ


# TODO: Test with serializer
def test_with_vcr():

    # Assemble
    serializer = CleanYAMLSerializer()
    serializer.register_cleaner(clean_token, uri='/api/foo')

    my_vcr = vcr.VCR(
        cassette_library_dir='cassettes',
        record_mode='once' if VCR_RECORD else 'none',
        match_on=['uri', 'method'],
    )
    my_vcr.register_serializer("cleanyaml", serializer)

    # Act
    # TODO: Serialize something with a token to clean, using vcr

    # Assert
    # TODO: Verify the VCR serialized YAML contains CLEANER_JWT_TOKEN
