from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os.path
def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname( __file__ ),p))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../BD/DB_pompiers.db'))
db = SQLAlchemy(app)