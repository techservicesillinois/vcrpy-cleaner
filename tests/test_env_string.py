import os
import pytest

from vcr_cleaner.cleaners.env_strings import clean_env_strings

ALWAYS_CLEAN= 'CLEAN ME,CLEAN THIS TOO'

def get_body_string(body):
    return {
        'response': {
            'body': {
                'string':body
            }
        }
    }

CLEAN_TEST_PARAMS = [
    ('CLEAN ME', 'CLEANED'),
    ('CLEAN THIS TOO', 'CLEANED'),
    ('CLEAN ME and CLEAN THIS TOO', 'CLEANED and CLEANED'),
    ('NOTHING TO CLEAN', 'NOTHING TO CLEAN'),
    (b'CLEAN ME', b'CLEAN ME'),  # Current expected behavior - may change
    (b'DEADBEEF', b'DEADBEEF'),  # Regression for #20
]


def get_body(body, request=""):
    return {
        'response': {
            'body': body
        },
        'request': {
            'body': request
        },
    }


@pytest.mark.parametrize('body,expected', CLEAN_TEST_PARAMS)
def test_clean_env_string_key(monkeypatch, body, expected):
    '''Test cases where there is a key named 'string' in 'body'.
    '''
    monkeypatch.setenv('CLEAN_STRINGS', ALWAYS_CLEAN)
    interaction = get_body_string(body)

    clean_env_strings(None, interaction['response'])

    result = interaction['response']['body']['string'] 
    assert result == expected
    assert interaction == get_body_string(expected)


@pytest.mark.parametrize('body,expected', CLEAN_TEST_PARAMS)
def test_clean_env_body(monkeypatch, body, expected):
    monkeypatch.setenv('CLEAN_STRINGS', ALWAYS_CLEAN)
    interaction = get_body(body)

    clean_env_strings(None, interaction['response'])

    result = interaction['response']['body']
    assert result == expected
    assert interaction == get_body(expected)


@pytest.mark.parametrize('body', 
                         (lambda: x for x,_ in CLEAN_TEST_PARAMS))
def test_env_unset(monkeypatch, body):
    """Nothing happens when the ENV variable is not set."""
    monkeypatch.setenv('CLEAN_STRINGS', ALWAYS_CLEAN)
    interaction = get_body(body)

    clean_env_strings(None, interaction['response'])

    result = interaction['response']['body']
    assert result == body 
    assert interaction == get_body(body)


@pytest.mark.parametrize('body,expected', CLEAN_TEST_PARAMS)
def test_clean_env_request(monkeypatch, body, expected):
    """Clean requests as well as responses"""
    monkeypatch.setenv('CLEAN_STRINGS', ALWAYS_CLEAN)
    interaction = get_body(body="", request=body)

    clean_env_strings(interaction['request'], None)

    result = interaction['request']['body']
    assert result == expected
    assert interaction == get_body(body= "", request=expected)

