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
    
class TypeDocument(db.Model):
    idType = db.Column(db.Integer, primary_key =True)
    nomType = db.Column(db.String(100))
    
class Document(db.Model):
    idDoc = db.Column(db.Integer, primary_key =True)
    nomDoc = db.Column(db.String(100))
    fichierDoc = db.Column(db.String(100))
    idType = db.Column(db.Integer, db.ForeignKey('typedocument.idType'))
    
class Tag(db.Model):
    idTag = db.Column(db.Integer, primary_key =True)
    nomTag = db.Column(db.String(100))
    niveauProtection = db.Column(db.Integer)
    couleurTag = db.Column(db.String(100))
    
def get_tags():
    return Tag.query.all()

def get_types():
    return TypeDocument.query.all()