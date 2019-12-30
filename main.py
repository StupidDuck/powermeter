import os
from dotenv import load_dotenv
from urllib.parse import urlencode
from functools import wraps
from authlib.integrations.flask_client import OAuth
from flask import Flask, request, redirect, url_for, session, jsonify, send_file, render_template, flash
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
        if 'profile' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated


@app.route('/')
@requires_auth
def index():
    meters = Meter.find_all(session['profile']['id'])
    return render_template('index.html.j2', meters=meters)


@app.route('/api/')
@requires_auth
def index_api():
    meters = Meter.find_all(session['profile']['id'])
    return jsonify([{
        'id': meter._id,
        'name': meter.name
     } for meter in meters])


@app.route('/login')
def login():
    if os.environ['FLASK_ENV'] == 'development':
        session['profile'] = {
            'id': 'auth0|6ca2578067456311c2de32be',
            'email': 'dev@asgaror.space'
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
        'id': userinfo['sub'],
        'email': userinfo['name'],
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
    if Meter.find(meter_id).user_id != session['profile']['id']:
        flash('Not allowed to do this !')
        return redirect(url_for('index'))
    _date = request.form.get('date')
    _value = float(request.form.get('value'))
    try:
        MeterReading(_date, _value, meter_id).save()
    except (TypeError, ValueError) as err:
        flash(err)
    return redirect(url_for('view', meter_id=meter_id))


@app.route('/meter/<int:id>/delete')
@requires_auth
def delete_meter(id):
    try:
        meter = Meter.find(id)
        if meter.user_id == session['profile']['id']:
            meter.delete()
        else:
            flash('Not allowed to do this !')
    except:
        flash('Error, action aborted !')
    finally:
        return redirect(url_for('index'))


@app.route('/meter/<int:meter_id>/view')
@requires_auth
def view(meter_id):
    return render_template('view.html.j2', meter_id=meter_id)


@app.route('/api/meter/<int:meter_id>/journal')
@requires_auth
def journal_api(meter_id):
    if Meter.find(meter_id).user_id != session['profile']['id']:
        flash('Not allowed to do this !')
        return redirect(url_for('index'))
    journal_obj = Journal(meter_id)
    days = 15
    return jsonify({
        'meter_id': meter_id,
        'journal': { 
            'entries': list(reversed([{
                'id': mr._id,
                'date': mr.date,
                'value': mr.value,
                'mean_consumption_per_day': mr.mean_consumption_per_day
            } for mr in journal_obj._mrs])),
            'days': days,
            'trend_last_days': journal_obj.trend_last_days(days),
            'mean': journal_obj.mean
        }
    })


# @app.route('/meter/<int:meter_id>/json')
# @requires_auth
# def json_chart_data(meter_id):
#     if Meter.find(meter_id).user_id != session['profile']['id']:
#         return jsonify({})
#     journal_obj = Journal(meter_id)

#     chart_data = {
#         'y_min': 0.0,
#         'y_max': 0.0,
#         'labels': [],
#         'values': []
#     }

#     for mr in journal_obj[1:]:
#         chart_data['labels'].append(mr.date)
#         chart_data['values'].append(mr.mean_consumption_per_day)

#     mean = journal_obj.mean
#     chart_max = max([mr.mean_consumption_per_day for mr in journal_obj])
#     chart_min = min([mr.mean_consumption_per_day for mr in journal_obj])
#     chart_data['y_max'] = chart_max + chart_max / 5
#     chart_data['y_min'] = chart_min + chart_min / 5

#     return jsonify({
#         'values': chart_data['values'],
#         'mean': mean,
#         'labels': chart_data['labels'],
#         'y_min': chart_data['y_min'],
#         'y_max': chart_data['y_max'],
#     })


@app.route('/meter/<int:meter_id>/journal/export')
@requires_auth
def export_csv(meter_id):
    meter = Meter.find(meter_id)
    if meter.user_id == session['profile']['id']:
        journal_obj = Journal(meter_id)
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
    meter = Meter.find(meter_id)
    if meter.user_id == session['profile']['id']:
        journal_obj = Journal(meter_id)
        journal_obj.import_csv(file)
    else:
        flash('Not allowed to do this !')
    return redirect(url_for('view', meter_id=meter_id))


@app.route('/mr/<int:id>/delete')
@requires_auth
def delete_mr(id):
    try:
        mr = MeterReading.find(id)
        meter = Meter.find(mr.meter_id)
        if meter.user_id == session['profile']['id']:
            mr.delete()
        else:
            flash('Not allowed to do this !')
        return redirect(url_for('view', meter_id=mr.meter_id))
    except:
        flash('Error, action aborted')
        return redirect(url_for('index'))
