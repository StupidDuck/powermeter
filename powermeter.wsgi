activate_this = '/home/pi/.local/share/virtualenvs/powermeter-cYxmiIoa/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys, os
sys.path.insert(0, '/home/pi/public_html/powermeter')
os.chdir('/home/pi/public_html/powermeter')

from dotenv import load_dotenv
load_dotenv()

# Prepare production ENV
os.environ['FLASK_ENV'] = 'production'
import random
os.environ['SECRET_KEY'] = random.getrandbits(128)

from main import app as application
