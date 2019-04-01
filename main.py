import os
from core.models.MeterReading import MeterReading
from core.models.MeterReadings import MeterReadings
from user import User
from functools import wraps
from datetime import datetime, date, timedelta
from urllib.parse import urlencode
from flask import Flask, request, redirect, url_for, render_template, flash, session, jsonify
from authlib.flask.client import OAuth

app = Flask(__name__)
oauth = OAuth(app)

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
app.secret_key = os.environ['SECRET_KEY']

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect(url_for('login'))
    return f(*args, **kwargs)

  return decorated

@app.route('/')
@requires_auth
def index():
    mrs = MeterReadings()
    days = 7
    trend = mrs.trend_last_days(days)
    mean = mrs.mean
    return render_template('index.html.j2', title='Powermeter', mean=mean, trend=trend, days=days)

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri="{}{}".format(request.url_root[0:-1], url_for('authorize')), audience='https://asgaror.eu.auth0.com/userinfo')

@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('index', _external=True), 'client_id': os.environ['AUTH0_CLIENT_ID']}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@app.route('/authorize')
def authorize():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
    'user_id': userinfo['sub'],
    'name': userinfo['name'],
    'picture': userinfo['picture']
    }
    return redirect(url_for('index'))

@app.route('/mrs', methods=['GET', 'POST'])
@requires_auth
def mrs():
    if (request.method == 'POST'):
        _date = request.form.get('date')
        _value = float(request.form.get('value'))
        try:
            MeterReading(_date, _value).create()
        except (TypeError, ValueError) as e:
            flash(e)

    mrs = MeterReadings()
    if len(mrs) > 1:
        mean = float("{0:.2f}".format(sum([mr.mean_consumption_per_day for mr in mrs[1:]]) / (len(mrs) - 1)))
    else:
        mean = 0.0

    return render_template('mrs.html.j2', title='Meter Readings',
                            mrs=mrs, mean=mean)

@app.route('/mrs/chart_data')
@requires_auth
def get_chart_data():
    mrs = MeterReadings()

    chart_data = {
        'y_min': 0.0,
        'y_max': 0.0,
        'labels': [],
        'values': []
    }

    try:
        for mr in mrs[1:]:
            chart_data['labels'].append(mr.date)
            chart_data['values'].append(mr.mean_consumption_per_day)

        mean = float("{0:.2f}".format(sum([mr.mean_consumption_per_day for mr in mrs[1:]]) / (len(mrs) - 1)))
        chart_max = max([mr.mean_consumption_per_day for mr in mrs])
        chart_data['y_max'] = chart_max + chart_max / 5
    except (ZeroDivisionError, IndexError):
        mean = 0.0
    return jsonify({
        'values': chart_data['values'],
        'mean': mean,
        'labels': chart_data['labels'],
        'y_min': chart_data['y_min'],
        'y_max': chart_data['y_max'],
    })

@app.route('/mr/<int:id>/delete')
@requires_auth
def delete_mr(id):
    MeterReading.get_by_id(id).delete()
    return redirect(url_for('mrs'))
