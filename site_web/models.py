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

class Grade(db.Model):
    idGrade = db.Column(db.Integer, primary_key =True)
    nomGrade = db.Column(db.String(10))

def get_grades():
    return Grade.query.all()

class Caserne(db.Model):
    idCas = db.Column(db.Integer, primary_key =True)
    nomCaserne = db.Column(db.String(100))
    adresseCaserne = db.Column(db.String(100))

def get_caserne():
    return Caserne.query.all()