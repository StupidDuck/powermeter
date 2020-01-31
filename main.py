import os
from dotenv import load_dotenv
from urllib.parse import urlencode
from functools import wraps
from authlib.integrations.flask_client import OAuth
import jwt
import json
from flask import Flask, request, redirect, url_for, session, jsonify, send_file, render_template, flash, make_response
from core.models import Meter, Journal, MeterReading

# .env not commited, so does nothing except in dev env
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
        token = get_auth_token()
        # if 'profile' not in session:
        #     return redirect(url_for('login'))
        if token is None:
            print('token is none')
        else:
            print(token)
            #return redirect(url_for('login'))
        # TODO : check if this token is valid (not tempered...)
        return f(*args, **kwargs)

    return decorated

def requires_scope(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'read:info' in args:
            return f(*args, **kwargs)
        else:
            print('no read:info scope')
            #return redirect(url_for('login'))

    return decorated


@app.route('/')
@requires_auth
def index():
    meters = Meter.find(user_id=session['profile']['id'])
    return render_template('index.html.j2', meters=meters)


@app.route('/api/')
@requires_auth
def index_api():
    meters = Meter.find(user_id=session['profile']['id'])
    return jsonify([{
        'id': meter._id,
        'name': meter.name
     } for meter in meters])


@app.route('/login')
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


@app.route('/logout')
def logout():
    session.clear()
    # if os.environ['FLASK_ENV'] == 'dev':
    #     return redirect(url_for('login'))
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
    session['jwt_payload'] = userinfo #does waht ???
    session['profile'] = {
        'id': userinfo['sub'],
        'email': userinfo['name'],
        'all': userinfo,
    }
    return redirect(url_for('index'))


@app.route('/meter', methods=['POST'])
@requires_auth
def meter():
    _name = request.form.get('name')
    try:
        Meter(session['profile']['id'], _name).save()
        return redirect(url_for('index'))
    except (TypeError, ValueError) as err:
        flash(err)


@app.route('/meter/<int:meter_id>', methods=['POST'])
@requires_auth
def post_journal(meter_id):
    meter = Meter.find(id=meter_id, user_id=session['profile']['id'])
    if meter is not None:
        _date = request.form.get('date')
        _value = float(request.form.get('value'))
    else:
        flash('Not allowed to do this !')
        return redirect(url_for('index'))
    try:
        MeterReading(_date, _value, meter_id).save()
    except (TypeError, ValueError) as err:
        flash(err)
    return redirect(url_for('view', meter_id=meter_id))


@app.route('/meter/<int:meter_id>/delete')
@requires_auth
def delete_meter(meter_id):
    try:
        meter = Meter.find(id=meter_id, user_id=session['profile']['id'])
        meter.delete()
    except:
        flash('Error, action aborted !')
    finally:
        return redirect(url_for('index'))


@app.route('/meter/<int:meter_id>/view')
@requires_auth
def view(meter_id):
    resp = journal_api(meter_id)
    if resp.status_code != 200:
        return redirect(url_for('index'))
    resp_json = resp.get_json()
    return render_template('view.html.j2', meter_id=resp_json['meter_id'], meter_name=resp_json['meter_name'], journal=resp_json['journal'])


@app.route('/api/meter/<int:meter_id>/journal')
@requires_auth
def journal_api(meter_id):
    meter = Meter.find(id=meter_id, user_id=session['profile']['id'])
    if meter is not None:
        journal_obj = Journal(meter._id)
        days = 15
        return jsonify({
            'meter_id': meter._id,
            'meter_name': meter.name,
            'journal': { 
                'entries': [{
                    'id': mr._id,
                    'date': mr.date,
                    'value': mr.value,
                    'mean_consumption_per_day': mr.mean_consumption_per_day
                } for mr in journal_obj._mrs],
                'days': days,
                'trend_last_days': journal_obj.trend_last_days(days),
                'mean': journal_obj.mean
            }
        })
    else:
        return make_response(jsonify({}), 404)


@app.route('/meter/<int:meter_id>/journal/export')
@requires_auth
def export_csv(meter_id):
    meter = Meter.find(id=meter_id, user_id=session['profile']['id'])
    if meter is not None:
        journal_obj = Journal(meter._id)
        filename = journal_obj.export_csv()
    else:
        flash('Not allowed to do this !')
    return send_file(filename,
                     mimetype="text/csv",
                     as_attachment=True,
                     attachment_filename="export.csv")


@app.route('/meter/<int:meter_id>/journal/import', methods=['POST'])
@requires_auth
def import_csv(meter_id):
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('view', meter_id=meter_id))
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('view', meter_id=meter_id))
    meter = Meter.find(id=meter_id, user_id=session['profile']['id'])
    if meter is not None:
        journal_obj = Journal(meter._id)
        journal_obj.import_csv(file)
    else:
        flash('Not allowed to do this !')
    return redirect(url_for('view', meter_id=meter_id))


@app.route('/mr/<int:mr_id>/delete')
@requires_auth
def delete_mr(mr_id):
    try:
        mr = MeterReading.find(id=mr_id, user_id=session['profile']['id'])
        mr.delete()
        return redirect(url_for('view', meter_id=mr.meter_id))
    except:
        flash('Error, action aborted')
        return redirect(url_for('index'))


@app.route('/client')
@requires_auth
@requires_scope('read:info')
def client():
    return 'Working !'


def get_auth_token():
    auth = request.headers.get("Authorization", None)

    if auth:
        if auth.split()[0].lower == "bearer":
            return auth.split()[1]
    return None