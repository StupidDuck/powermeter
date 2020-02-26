import os
from urllib.parse import urlencode
from urllib.request import urlopen
from functools import wraps
import jwt
import json
from flask import Blueprint, request, redirect, session, url_for, make_response, jsonify, current_app
from authlib.integrations.flask_client import OAuth


auth = Blueprint('auth', __name__)
oauth = OAuth(current_app)
auth0 = oauth.register(
    'auth0',
    client_id=os.environ['AUTH0_CLIENT_ID'],
    client_secret=os.environ['AUTH0_CLIENT_SECRET'],
    api_base_url='https://asgaror.eu.auth0.com',
    access_token_url='https://asgaror.eu.auth0.com/oauth/token',
    authorize_url='https://asgaror.eu.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)


@auth.route('/login')
def login():
    # if os.environ['FLASK_ENV'] == 'development':
    #     session['profile'] = {
    #         'id': 'auth0|6ca2578067456311c2de32be',
    #         'email': 'dev@asgaror.space'
    #     }
    #     return redirect(url_for('index'))
    return auth0.authorize_redirect(
        redirect_uri="{}{}".format(request.url_root[0:-1], '/authorize'),
        audience='https://asgaror.eu.auth0.com/userinfo')


@auth.route('/logout')
def logout():
    session.clear()
    # if os.environ['FLASK_ENV'] == 'dev':
    #     return redirect(url_for('login'))
    params = {'returnTo': url_for('index', _external=True),
              'client_id': os.environ['AUTH0_CLIENT_ID']}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@auth.route('/authorize')
def authorize():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'id': userinfo['sub'],
        'email': userinfo['name'],
        'all': userinfo,
    }
    return redirect(url_for('index'))


def get_auth_token():
    auth_header = request.headers.get("Authorization", None)

    if auth_header:
        if auth_header.split()[0].lower() == "bearer":
            return auth_header.split()[1]
    return None


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # If regular user access...
        if 'profile' in session:
            return f(*args, **kwargs)
        # If client auth
        token = get_auth_token()
        if token is None:
            return redirect(url_for('auth.login'))
        unverified_token = jwt.get_unverified_header(token)
        jwksurl = urlopen('https://asgaror.eu.auth0.com/.well-known/jwks.json')
        jwks = json.loads(jwksurl.read())

        public_keys = {}
        for jwk in jwks['keys']:
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
        kid = unverified_token['kid']
        key = public_keys[kid]

        if public_keys:
            try:
                payload = jwt.decode(token, key=key, algorithms=['RS256'], audience='powermeter-api')
                # session['tokenjwt_payload'] = payload
                return f(*args, **kwargs)
            except:
                return make_response(jsonify({}), 401)

    return decorated


def requires_scopes(scopes):
    def call(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_auth_token()
            if not token:
                return f'A token is needed...'
            claims = jwt.decode(token, verify=False)
            if claims.get('scope'):
                token_scopes = claims['scope'].split()
                for scope in scopes:
                    if scope not in token_scopes:
                        return f'Scope : \'{scope}\' needed !'
            else:
                return f'A scope is needed !'
            return f(*args, **kwargs)
        return decorated
    return call
