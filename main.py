import os
from flask import Flask, request, redirect, url_for, render_template, flash, session, jsonify
from core.models.Journal import Journal
from core.models.MeterReading import MeterReading
from functools import wraps
from datetime import datetime, date, timedelta
from urllib.parse import urlencode
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
      return redirect(url_for('login'))
    return f(*args, **kwargs)

  return decorated

@app.route('/')
@requires_auth
def index():
    journal = Journal()
    days = 7
    trend = journal.trend_last_days(days)
    mean = journal.mean
    return render_template('index.html.j2', title='Powermeter', mean=mean, trend=trend, days=days)

@app.route('/login')
def login():
    if os.environ['FLASK_ENV'] == 'dev':
        session['profile'] = {
            'name': 'DEV'
        }
        return redirect(url_for('index'))
    return auth0.authorize_redirect(redirect_uri="{}{}".format(request.url_root[0:-1], url_for('authorize')), audience='https://asgaror.eu.auth0.com/userinfo')

@app.route('/logout')
def logout():
    session.clear()
    if os.environ['FLASK_ENV'] == 'dev':
        return redirect(url_for('login'))
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

@app.route('/journal', methods=['GET', 'POST'])
@requires_auth
def journal():
    if (request.method == 'POST'):
        _date = request.form.get('date')
        _value = float(request.form.get('value'))
        try:
            MeterReading(_date, _value).save()
        except (TypeError, ValueError) as e:
            flash(e)

    journal = Journal()
    mean = journal.mean

    return render_template('journal.html.j2', title='Meter Readings',
                            journal=journal, mean=mean)

@app.route('/journal/chart_data')
@requires_auth
def get_chart_data():
    journal = Journal()

    chart_data = {
        'y_min': 0.0,
        'y_max': 0.0,
        'labels': [],
        'values': []
    }

    for mr in journal[1:]:
        chart_data['labels'].append(mr.date)
        chart_data['values'].append(mr.mean_consumption_per_day)

    mean = journal.mean
    chart_max = max([mr.mean_consumption_per_day for mr in journal])
    chart_data['y_max'] = chart_max + chart_max / 5

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
    MeterReading.find(id).delete()
    return redirect(url_for('journal'))
