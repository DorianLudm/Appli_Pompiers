from .app import db

class Utilisateur(db.Model):
    idUtilisateur = db.Column(db.Integer, primary_key =True)
    nomUtilisateur = db.Column(db.String(100))
    prenomUtilisateur = db.Column(db.String(100))
    identifiant = db.Column(db.String(100))
    mdp = db.Column(db.String(100))
    idGrade = db.Column(db.Integer)
    idRole = db.Column(db.Integer)
    idCas = db.Column(db.Integer)
    