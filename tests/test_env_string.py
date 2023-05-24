import os
import pytest

from vcr_cleaner.cleaners.env_strings import clean_env_strings


def get_interaction(body):
    return {
        'response': {
            'body': {
                'string':body
            }
        }
    }


@pytest.mark.parametrize('body,expected', [
    ('CLEAN ME', 'CLEANED'),
    ('CLEAN THIS TOO', 'CLEANED'),
    ('CLEAN ME and CLEAN THIS TOO', 'CLEANED and CLEANED'),
    ('NOTHING TO CLEAN', 'NOTHING TO CLEAN'),
    (b'DEADBEEF', b'DEADBEEF'),
])
def test_clean_env_string(monkeypatch, body, expected):
    monkeypatch.setenv('CLEAN_STRINGS', 'CLEAN ME,CLEAN THIS TOO')

    interaction = get_interaction(body)
    clean_env_strings(None, interaction['response'])
    result = interaction['response']['body']['string'] 

    assert result == expected
