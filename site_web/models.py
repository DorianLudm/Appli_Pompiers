from .app import db
from sqlalchemy import func

class Utilisateur(db.Model):
    idUtilisateur = db.Column(db.Integer, primary_key =True)
    nomUtilisateur = db.Column(db.String(100))
    prenomUtilisateur = db.Column(db.String(100))
    identifiant = db.Column(db.String(100))
    mdp = db.Column(db.String(100))
    idGrade = db.Column(db.Integer, db.ForeignKey('Grade.idGrade'))
    idRole = db.Column(db.Integer, db.ForeignKey('Role.idRole'))
    idCas = db.Column(db.Integer, db.ForeignKey('Caserne.idCas'))
    
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

