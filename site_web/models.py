from .app import db
from .app import login_manager
from flask_login import UserMixin, current_user


class Utilisateur(db.Model, UserMixin):
    idUtilisateur = db.Column(db.Integer, primary_key =True)
    nomUtilisateur = db.Column(db.String(100))
    prenomUtilisateur = db.Column(db.String(100))
    identifiant = db.Column(db.String(100))
    mdp = db.Column(db.String(100))
    idGrade = db.Column(db.Integer)
    idRole = db.Column(db.Integer)
    idCas = db.Column(db.Integer)
    
    def get_id(self):
        return str(self.idUtilisateur)

class Grade(db.Model):
    idGrade = db.Column(db.Integer, primary_key =True)
    nomGrade = db.Column(db.String(10))

def get_grades():
    return Grade.query.all()

class Caserne(db.Model):
    idCas = db.Column(db.Integer, primary_key =True)
    nomCaserne = db.Column(db.String(100))
    adresseCaserne = db.Column(db.String(100))

class Role(db.Model):
    idRole = db.Column(db.Integer, primary_key =True)
    nomRole = db.Column(db.String(100))

def get_nom_role(idRole):
    return Role.query.filter_by(idRole=current_user.idRole).first().nomRole

def get_caserne():
    return Caserne.query.all()

def get_nom_grade(idGrade):
    return Grade.query.filter_by(idGrade=current_user.idGrade).first().nomGrade

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

def informations_utlisateurs():
    util = dict()
    util['nom'] = current_user.nomUtilisateur
    util['prenom'] = current_user.prenomUtilisateur
    util['grade'] = get_nom_grade(current_user.idGrade)
    util['role'] = get_nom_role(current_user.idRole)
    return util
