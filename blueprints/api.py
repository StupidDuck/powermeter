from flask import Blueprint, session, jsonify, make_response
from core.models import Meter, Journal
from .auth import requires_auth


api = Blueprint('api', __name__)


@api.route('/api/')
@requires_auth
def meters():
    _meters = Meter.find(user_id=session['profile']['id'])
    return jsonify([{
        'id': meter.id,
        'name': meter.name
     } for meter in _meters])


@api.route('/api/meter/<int:meter_id>/journal')
@requires_auth
def journal(meter_id):
    meter = Meter.find(_id=meter_id, user_id=session['profile']['id'])
    if meter is not None:
        journal_obj = Journal(meter.id)
        days = 15
        return jsonify({
            'meter_id': meter.id,
            'meter_name': meter.name,
            'journal': {
                'entries': [{
                    'id': mr.id,
                    'date': mr.date,
                    'value': mr.value,
                    'mean_consumption_per_day': mr.mean_consumption_per_day
                } for mr in journal_obj.mrs],
                'days': days,
                'trend_last_days': journal_obj.trend_last_days(days),
                'mean': journal_obj.mean
            }
        })
    else:
        return make_response(jsonify({}), 404)
