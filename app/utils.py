from urllib.parse import urljoin, urlparse

from flask import request


def get_or_create(model, **kwargs):
    ''' Returns an instance of model and whether or not it already existed in a tuple. '''
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        return instance, True


def is_safe_url(target):
    ''' Checks if an URL is safe. '''
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http',
                               'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    ''' Returns the redirect target. '''
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        elif is_safe_url(target):
            return target
