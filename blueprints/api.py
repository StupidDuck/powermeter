from flask import Blueprint, jsonify, make_response, request, send_file
from core.viewmodel import MeterViewModel, JournalViewModel
from .auth import requires_auth


api = Blueprint('api', __name__)


@api.route('/api/meter')
@requires_auth
def meters(uid):
    _meters = MeterViewModel(user_id=uid).get()
    return jsonify(_meters)


@api.route('/api/meter', methods=['POST'])
@requires_auth
def add_meter(uid):
    _name = request.form.get('name')
    try:
        return jsonify({
            'id': MeterViewModel(user_id=uid).save(name=_name)
        })
    except (TypeError, ValueError):
        return make_response(jsonify({}), 404)


@api.route('/api/meter', methods=['DELETE'])
@requires_auth
def delete_meter(uid):
    try:
        _meter_id = request.form.get('meter_id')
        return jsonify({
            'id': MeterViewModel(user_id=uid).delete(_meter_id)
        })
    except (TypeError, ValueError):
        return make_response(jsonify({}), 404)


@api.route('/api/meter/<int:meter_id>/index', methods=['POST'])
@requires_auth
def add_index(uid, meter_id):
    try:
        _date = request.form.get('date')
        _value = float(request.form.get('value'))
        return jsonify({
            'id': JournalViewModel(user_id=uid, meter_id=meter_id).save_index(_date, _value)
        })
    except (TypeError, ValueError):
        make_response(jsonify({}), 404)


@api.route('/api/meter/<int:meter_id>/index', methods=['DELETE'])
@requires_auth
def delete_index(uid, meter_id):
    try:
        _index_id = int(request.form.get('index_id'))
        return jsonify({
            'id': JournalViewModel(user_id=uid, meter_id=meter_id).delete_index(_index_id)
        })
    except (TypeError, ValueError):
        make_response(jsonify({}), 404)


@api.route('/api/meter/<int:meter_id>/journal')
@requires_auth
def journal(uid, meter_id):
    try:
        return jsonify(JournalViewModel(user_id=uid, meter_id=meter_id).get())
    except (TypeError, ValueError):
        return make_response(jsonify({}), 404)


@api.route('/api/meter/<int:meter_id>/journal/export')
@requires_auth
def export_journal(uid, meter_id):
    try:
        filename = JournalViewModel(user_id=uid, meter_id=meter_id).export_csv()
        return send_file(filename,
                         mimetype="text/csv",
                         as_attachment=True,
                         attachment_filename="export.csv")
    except (TypeError, ValueError):
        return make_response(jsonify({}), 404)


def import_journal(uid, meter_id):
    pass
# @app.route('/meter/<int:meter_id>/journal/import', methods=['POST'])
# @auth.requires_auth
# def import_csv(meter_id):
#     if 'file' not in request.files:
#         flash('No file selected')
#         return redirect(url_for('view', meter_id=meter_id))
#     file = request.files['file']
#     if file.filename == '':
#         flash('No file selected')
#         return redirect(url_for('view', meter_id=meter_id))
#     _meter = Meter.find(_id=meter_id, user_id=session['profile']['id'])
#     if _meter is not None:
#         journal_obj = Journal(meter.id)
#         journal_obj.import_csv(file)
#     else:
#         flash('Not allowed to do this !')
#     return redirect(url_for('view', meter_id=meter_id))
