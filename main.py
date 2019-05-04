"""
This webapp is aiming to log your electrical consumption.
Usefull when used with photovoltaic solar panels.
"""

import os
from urllib.parse import urlencode
from functools import wraps
from authlib.flask.client import OAuth
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, render_template, flash, session, jsonify, send_file
from core.models import Journal, MeterReading

load_dotenv()

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

@app.route('/test')
def test():
    print(url_for('login'))
    print(request.url_root)
    print(request)

@app.route('/')
@requires_auth
def index():
    # TO_DO : include mean and trends on js chart ?
    journal_obj = Journal()
    days = 7
    trend = journal_obj.trend_last_days(days)
    mean = journal_obj.mean
    return render_template('index.html.j2', title='Powermeter', mean=mean, trend=trend, days=days)

@app.route('/login')
def login():
    if os.environ['FLASK_ENV'] == 'development':
        session['profile'] = {
            'name': 'DEV'
        }
        return redirect(url_for('index'))
    return auth0.authorize_redirect(
        redirect_uri="{}{}".format(request.url_root[0:-1], '/authorize'),
        audience='https://asgaror.eu.auth0.com/userinfo')

@app.route('/logout')
def logout():
    session.clear()
    if os.environ['FLASK_ENV'] == 'dev':
        return redirect(url_for('login'))
    params = {'returnTo': url_for('index', _external=True),
              'client_id': os.environ['AUTH0_CLIENT_ID']}
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
    if request.method == 'POST':
        _date = request.form.get('date')
        _value = float(request.form.get('value'))
        try:
            MeterReading(_date, _value).save()
        except (TypeError, ValueError) as err:
            flash(err)

    journal_obj = Journal()
    mean = journal_obj.mean

    return render_template('journal.html.j2', title='Meter Readings',
                           journal=journal_obj, mean=mean)

@app.route('/journal/chart_data')
@requires_auth
def get_chart_data():
    journal_obj = Journal()

    chart_data = {
        'y_min': 0.0,
        'y_max': 0.0,
        'labels': [],
        'values': []
    }

    for mr in journal_obj[1:]:
        chart_data['labels'].append(mr.date)
        chart_data['values'].append(mr.mean_consumption_per_day)

    mean = journal_obj.mean
    chart_max = max([mr.mean_consumption_per_day for mr in journal_obj])
    chart_data['y_max'] = chart_max + chart_max / 5

    return jsonify({
        'values': chart_data['values'],
        'mean': mean,
        'labels': chart_data['labels'],
        'y_min': chart_data['y_min'],
        'y_max': chart_data['y_max'],
    })
@app.route('/journal/export')
@requires_auth
def export():
    journal_obj = Journal()
    path = journal_obj.export_csv()
    return send_file(path,
                     mimetype="text/csv",
                     as_attachment=True,
                     attachment_filename="export.csv")
    
@app.route('/mr/<int:id>/delete')
@requires_auth
def delete_mr(mr_id):
    MeterReading.find(mr_id).delete()
    return redirect(url_for('journal'))
