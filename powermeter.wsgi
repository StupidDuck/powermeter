import sys, os
sys.path.insert(0, '/home/pi/public_html/powermeter')
os.chdir('/home/pi/public_html/powermeter')

from dotenv import load_dotenv
load_dotenv()

#TODO : automatiser l'installation de nouvelles lib / update avec pip et requirements.txt

# Prepare production ENV
os.environ['FLASK_ENV'] = 'production'
os.environ['DB_FILENAME'] = 'irs.db'
import random
os.environ['SECRET_KEY'] = "{}".format(random.getrandbits(128))

from main import app as application
