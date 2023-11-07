from flask_bootstrap import Bootstrap5
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os.path
def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname( __file__ ),p))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('../BD/DB_Pompiers.db'))
db = SQLAlchemy(app)
app.config['BOOTSTRAP_SERVE_LOCAL']=True
bootstrap = Bootstrap5(app)
