from .app import db
from .app import login_manager


class Utilisateur(db.Model):
    idUtilisateur = db.Column(db.Integer, primary_key =True, autoincrement=True)
    nomUtilisateur = db.Column(db.String(100))
    prenomUtilisateur = db.Column(db.String(100))
    identifiant = db.Column(db.String(100))
    mdp = db.Column(db.String(100))
    idGrade = db.Column(db.Integer)
    idRole = db.Column(db.Integer)
    idCas = db.Column(db.Integer)

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

def max_id_utilisateur():
    max_id = db.session.query(db.func.max(Utilisateur.idUtilisateur)).scalar()
    if max_id is None:
        return 0
    else:
        return max_id