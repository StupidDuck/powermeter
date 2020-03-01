from flask import Blueprint, render_template, redirect, url_for, request, flash
from core.viewmodel import MeterViewModel, JournalViewModel
from .auth import requires_auth


view = Blueprint('view', __name__)


@view.route('/')
@requires_auth
def index(uid):
    index_view_model = MeterViewModel(user_id=uid).get()
    return render_template('index.html.j2', model=index_view_model)


@view.route('/meter', methods=['POST'])
@requires_auth
def add_meter(uid):
    try:
        _name = request.form.get('name')
        _id = MeterViewModel(uid).save(_name)
        return redirect(url_for('view.meter', meter_id=_id))
    except (TypeError, ValueError) as err:
        flash(f"Error : {err}")
        return redirect(url_for('view.index'))


@view.route('/meter/delete', methods=['POST'])
@requires_auth
def delete_meter(uid):
    _meter_id = int(request.form.get('meter-id'))
    MeterViewModel(uid).delete(_meter_id)
    return redirect(url_for('view.index'))


@view.route('/meter/<int:meter_id>')
@requires_auth
def meter(uid, meter_id):
    journal_view_model = JournalViewModel(user_id=uid, meter_id=meter_id).get()
    return render_template('view.html.j2', model=journal_view_model)


@view.route('/meter/<int:meter_id>', methods=['POST'])
@requires_auth
def add_index(uid, meter_id):
    try:
        _value = float(request.form.get('value'))
        _date = request.form.get('date')
        JournalViewModel(user_id=uid, meter_id=meter_id).save_index(_value, _date)
    except (TypeError, ValueError) as err:
        flash(f"Error : {err}")
    finally:
        return redirect(url_for('view.meter', meter_id=meter_id))


@view.route('/meter/<int:meter_id>/delete', methods=['POST'])
@requires_auth
def delete_index(uid, meter_id):
    try:
        _index_id = int(request.form.get('index-id'))
        JournalViewModel(user_id=uid, meter_id=meter_id).delete_index(_index_id)
    except (TypeError, ValueError) as err:
        flash(f"Error : {err}")
    finally:
        return redirect(url_for('view.meter', meter_id=meter_id))
