from flask import redirect, url_for
from flask_wtf import Form
from wtforms import HiddenField

from app.utils import get_redirect_target, is_safe_url

class RedirectForm(Form):
    """
    Redirects the client to a certain page on submit.

    Use the redirect method to set the redirect URL, as long as the URL is secure.
    If it is not set, the default will be the previous page.

    """

    next = HiddenField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ""

    def redirect(self, endpoint="index", **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)

        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))