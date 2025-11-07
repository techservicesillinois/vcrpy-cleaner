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
