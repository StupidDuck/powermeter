import os
from dotenv import load_dotenv
from flask import Flask
from blueprints import auth, api, view


# .env not committed, so does nothing except in dev env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.register_blueprint(auth.auth)
app.register_blueprint(api.api)
app.register_blueprint(view.view)


# @app.route('/client')
# @requires_auth
# @requires_scopes(['read:info'])
# def client(uid):
#     return jsonify({
#         'user_id': uid,
#         'meters': [
#             {
#                 'id': 1,
#                 'name': 'meter_one'
#             },{
#                 'id': 2,
#                 'name': 'meter_two'
#             },
#         ]
#     })
