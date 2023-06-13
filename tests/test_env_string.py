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


@pytest.mark.parametrize('body,expected', [
    ('CLEAN ME', 'CLEANED'),
    ('CLEAN THIS TOO', 'CLEANED'),
    ('CLEAN ME and CLEAN THIS TOO', 'CLEANED and CLEANED'),
    ('NOTHING TO CLEAN', 'NOTHING TO CLEAN'),
])
def test_clean_env_string_key(monkeypatch, body, expected):
    '''Test cases where there is a key named 'string' in 'body'.
    '''
    monkeypatch.setenv('CLEAN_STRINGS', ALWAYS_CLEAN)

    interaction = get_body_string(body)
    clean_env_strings(None, interaction['response'])
    result = interaction['response']['body']['string'] 

    assert result == expected
    assert interaction == get_body_string(expected)



def get_body(body):
    return {
        'response': {
            'body': body
        }
    }



@pytest.mark.parametrize('body,expected', [
    ('CLEAN ME', 'CLEANED'),
    ('CLEAN THIS TOO', 'CLEANED'),
    ('CLEAN ME and CLEAN THIS TOO', 'CLEANED and CLEANED'),
    ('NOTHING TO CLEAN', 'NOTHING TO CLEAN'),
    (b'DEADBEEF', b'DEADBEEF'),
    (b'CLEAN ME', b'CLEAN ME'),
])
def test_clean_env_string(monkeypatch, body, expected):
    monkeypatch.setenv('CLEAN_STRINGS', ALWAYS_CLEAN)

    interaction = get_body(body)
    clean_env_strings(None, interaction['response'])
    result = interaction['response']['body']

    assert result == expected
    assert interaction == get_body(expected)


@pytest.mark.parametrize('body,expected', [
    ('CLEAN ME', 'CLEAN ME'),
    ('CLEAN THIS TOO', 'CLEAN THIS TOO'),
    (b'DEADBEEF', b'DEADBEEF'),
    (b'CLEAN ME', b'CLEAN ME'),
])
def test_env_unset(monkeypatch, body, expected):
    interaction = get_body(body)
    clean_env_strings(None, interaction['response'])
    result = interaction['response']['body']

    assert result == expected
    assert interaction == get_body(expected)

