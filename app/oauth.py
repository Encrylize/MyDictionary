import os
from flask import session

from app import oauth

facebook = oauth.remote_app(
    "facebook",
    base_url="https://graph.facebook.com/",
    request_token_url=None,
    access_token_url="/oauth/access_token",
    authorize_url="https://facebook.com/dialog/oauth",
    consumer_key=os.getenv("MYDICTIONARY_FACEBOOK_APP_ID"),
    consumer_secret=os.getenv("MYDICTIONARY_FACEBOOK_APP_SECRET"),
    request_token_params={"scope": "email"}
)

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get("oauth_token")