from urllib.parse import urlparse, urljoin
from flask import request

def get_or_create(model, **kwargs):
    """ Returns an instance of model and whether or not it already existed in a tuple. """
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        return instance, True

def is_safe_url(target):
    """ Checks if an URL is safe. """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc