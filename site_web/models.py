from .app import db, login_manager
from flask_login import UserMixin, current_user
from sqlalchemy import func


class Caserne(db.Model):
    idCas = db.Column(db.Integer, primary_key =True)
    nomCaserne = db.Column(db.String(100))
    adresseCaserne = db.Column(db.String(100))

    def get_id(self):
      return str(self.idCas)

class Grade(db.Model):
    idGrade = db.Column(db.Integer, primary_key =True)
    nomGrade = db.Column(db.String(100))

    def get_id(self):
        return str(self.idGrade)

class Role(db.Model):
    idRole = db.Column(db.Integer, primary_key =True)
    nomRole = db.Column(db.String(100))

    def get_id(self):
      return str(self.idRole)

class Utilisateur(db.Model, UserMixin):
    idUtilisateur = db.Column(db.Integer, primary_key =True)
    nomUtilisateur = db.Column(db.String(100))
    prenomUtilisateur = db.Column(db.String(100))
    identifiant = db.Column(db.String(100))
    mdp = db.Column(db.String(100))
    idGrade = db.Column(db.Integer, db.ForeignKey('grade.idGrade'))
    idRole = db.Column(db.Integer, db.ForeignKey('role.idRole'))
    idCas = db.Column(db.Integer, db.ForeignKey('caserne.idCas'))
    
    def get_id(self):
      return str(self.idUtilisateur)
    
    def __repr__(self):
        return f'Utilisateur {self.idUtilisateur} : {self.nomUtilisateur} {self.prenomUtilisateur} \tid : {self.identifiant} '
    
class TypeDocument(db.Model):
    idType = db.Column(db.Integer, primary_key =True)
    nomType = db.Column(db.String(100))
    
class Document(db.Model):
    idDoc = db.Column(db.Integer, primary_key =True)
    nomDoc = db.Column(db.String(100))
    fichierDoc = db.Column(db.String(100))
    idType = db.Column(db.Integer, db.ForeignKey('type_document.idType'))
    
class Tag(db.Model):
    idTag = db.Column(db.Integer, primary_key =True)
    nomTag = db.Column(db.String(100))
    niveauProtection = db.Column(db.Integer)
    couleurTag = db.Column(db.String(100))
    
class DocumentTag(db.Model):
    idTag = db.Column(db.Integer, db.ForeignKey('tag.idTag'), primary_key = True)
    idDoc = db.Column(db.Integer, db.ForeignKey('document.idDoc'), primary_key = True)
    
def get_tags():
    return Tag.query.order_by(Tag.nomTag).all()

def get_tag(nomTag):
    return Tag.query.filter(Tag.nomTag.like('%' + nomTag + '%')).first()

def get_tag_nom(nomTag):
    return Tag.query.filter(Tag.nomTag == nomTag).first().idTag

def get_tag_idDoc(idDoc):
    return DocumentTag.query.filter(DocumentTag.idDoc == idDoc).all()

def get_types():
    return TypeDocument.query.all()

def get_documents():
    return Document.query.all()

def get_document_types(idTypeDoc, active_tags,filtre_texte):
    document = Document.query.filter(Document.idType == idTypeDoc).filter(Document.nomDoc.like('%' + filtre_texte + '%')).all()
    resultat = []
    if active_tags != []:
        for doc in document:
            est_present = True
            for tag in active_tags:
                if not DocumentTag.query.filter(DocumentTag.idTag == tag.idTag).filter(DocumentTag.idDoc == doc.idDoc).all():
                    est_present = False
            if est_present:
                resultat.append(doc)
        return resultat 
    return document

def get_document_id(idDoc):
    return Document.query.get(idDoc)

def get_utilisateurs():
    return Utilisateur.query.order_by(func.upper(Utilisateur.nomUtilisateur), func.upper(Utilisateur.prenomUtilisateur)).all()
 

def get_grades():
    return Grade.query.all()

def get_utilisateur(idUtilisateur):
    return Utilisateur.query.get(idUtilisateur)

def get_nom_role(idRole):
    return Role.query.filter_by(idRole=current_user.idRole).first().nomRole

def get_casernes():
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
