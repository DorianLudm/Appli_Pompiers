from .app import db, login_manager
from sqlalchemy import func
from flask_login import UserMixin


class Utilisateur(db.Model, UserMixin):
    idUtilisateur = db.Column(db.Integer, primary_key =True)
    nomUtilisateur = db.Column(db.String(100))
    prenomUtilisateur = db.Column(db.String(100))
    identifiant = db.Column(db.String(100))
    mdp = db.Column(db.String(100))
    idGrade = db.Column(db.Integer, db.ForeignKey('Grade.idGrade'))
    idRole = db.Column(db.Integer, db.ForeignKey('Role.idRole'))
    idCas = db.Column(db.Integer, db.ForeignKey('Caserne.idCas'))
    
    def get_id(self):
      return str(self.idUtilisateur)
    
class Caserne(db.Model):
    idCas = db.Column(db.Integer, primary_key =True)
    nomCaserne = db.Column(db.String(100))
    adresseCaserne = db.Column(db.String(100))

class Grade(db.Model):
    idGrade = db.Column(db.Integer, primary_key =True)
    nomGrade = db.Column(db.String(100))

class Role(db.Model):
    idRole = db.Column(db.Integer, primary_key =True)
    nomRole = db.Column(db.String(100))

def get_utilisateurs():
    return Utilisateur.query.order_by(func.upper(Utilisateur.nomUtilisateur), func.upper(Utilisateur.prenomUtilisateur)).all()
 

def get_grades():
    return Grade.query.all()

def get_casernes():
    return Caserne.query.all()

@login_manager.user_loader
def load_user(username):
    return Utilisateur.query.get(username)

def max_id_utilisateur():
    max_id = db.session.query(db.func.max(Utilisateur.idUtilisateur)).scalar()
    if max_id is None:
        return 0
    else:
        return max_id

def get_identifiant_utilisateur(user):
    return Utilisateur.query.filter_by(identifiant=user).first()
