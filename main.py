import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for, session, jsonify, send_file, render_template, flash, make_response
from blueprints import api, auth
from core.models import Meter, Journal, MeterReading


# .env not committed, so does nothing except in dev env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.register_blueprint(auth.auth)
app.register_blueprint(api.api)


@app.route('/')
@auth.requires_auth
def index():
    meters = api.meters().get_json()
    return render_template('index.html.j2', meters=meters)


@app.route('/meter', methods=['POST'])
@auth.requires_auth
def meter():
    _name = request.form.get('name')
    try:
        Meter(session['profile']['id'], _name).save()
        return redirect(url_for('index'))
    except (TypeError, ValueError) as err:
        flash(err)


@app.route('/meter/<int:meter_id>', methods=['POST'])
@auth.requires_auth
def post_journal(meter_id):
    _meter = Meter.find(_id=meter_id, user_id=session['profile']['id'])
    if _meter is not None:
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
@auth.requires_auth
def delete_meter(meter_id):
    try:
        _meter = Meter.find(_id=meter_id, user_id=session['profile']['id'])
        _meter.delete()
    except:
        flash('Error, action aborted !')
    finally:
        return redirect(url_for('index'))


@app.route('/meter/<int:meter_id>/view')
@auth.requires_auth
def view(meter_id):
    resp = api.journal(meter_id)
    if resp.status_code != 200:
        return redirect(url_for('index'))
    resp_json = resp.get_json()
    return render_template('view.html.j2', meter_id=resp_json['meter_id'], meter_name=resp_json['meter_name'], journal=resp_json['journal'])


@app.route('/meter/<int:meter_id>/journal/export')
@auth.requires_auth
def export_csv(meter_id):
    _meter = Meter.find(_id=meter_id, user_id=session['profile']['id'])
    if _meter is None:
        flash('Not allowed to do this !')
        redirect(url_for('index'))
    journal_obj = Journal(meter.id)
    filename = journal_obj.export_csv()
    return send_file(filename,
                     mimetype="text/csv",
                     as_attachment=True,
                     attachment_filename="export.csv")


@app.route('/meter/<int:meter_id>/journal/import', methods=['POST'])
@auth.requires_auth
def import_csv(meter_id):
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('view', meter_id=meter_id))
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('view', meter_id=meter_id))
    _meter = Meter.find(_id=meter_id, user_id=session['profile']['id'])
    if _meter is not None:
        journal_obj = Journal(meter.id)
        journal_obj.import_csv(file)
    else:
        flash('Not allowed to do this !')
    return redirect(url_for('view', meter_id=meter_id))


@app.route('/mr/<int:mr_id>/delete')
@auth.requires_auth
def delete_mr(mr_id):
    try:
        mr = MeterReading.find(_id=mr_id, user_id=session['profile']['id'])
        mr.delete()
        return redirect(url_for('view', meter_id=mr.meter_id))
    except:
        flash('Error, action aborted')
        return redirect(url_for('index'))


@app.route('/client')
@auth.requires_auth
@auth.requires_scopes(['read:info'])
def client():
    return jsonify({
        'meters': [
            {
                'id': 1,
                'name': 'meter_one'
            },{
                'id': 2,
                'name': 'meter_two'
            },
        ]
    })