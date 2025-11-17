import json
import re


def clean_uri(old: str, new: str):
    """Returns a cleaner function that replaces the request URI
    string with all occurrences of substring old replaced by new.

    from vcr_cleaner.cleaners import clean_uri
    from vcr_cleaner import CleanYAMLSerializer as CYS

    CYS.register_cleaner(clean_uri('example', 'CLEANED'))
    """
    def clean_uri(request: dict, response: dict):
        if "uri" not in request.keys():
            return request
        request['uri'] = request['uri'].replace(old, new)
        return request

    clean_uri.__doc__ = f"Replaces the request URI string with all " \
        f"occurrences of substring '{old}' replaced by '{new}'."
    return clean_uri


def _clean_dict_hostnames(message: dict, rule: str, replacement: str):
    '''Update the dictionary with rule matches replaced.'''
    cleaned = re.sub(rule, replacement, json.dumps(message))

    # Update the original dict
    message.clear()
    message.update(json.loads(cleaned))


def clean_domains(domain: str, replacement: str = 'cleaned.example.edu'):
    '''Replace anything that looks like the given domain.'''
    rule = f"/[^/]*{domain.replace('.', r'\.')}"
    rep = f"/{replacement}"

    def wrapper(request: dict, response: dict):
        _clean_dict_hostnames(request, rule, rep)
        _clean_dict_hostnames(response, rule, rep)

    wrapper.__doc__ = clean_domains.__doc__

    return wrapper
