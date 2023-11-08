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
    
class DocumentTag(db.Model):
    idTag = db.Column(db.Integer, db.ForeignKey('tag.idTag'), primary_key = True)
    idDoc = db.Column(db.Integer, db.ForeignKey('document.idDoc'), primary_key = True)
    
def get_tags():
    return Tag.query.order_by(Tag.nomTag).all()

def get_tag(nomTag):
    return Tag.query.filter(Tag.nomTag.like('%' + nomTag + '%')).first().nomTag

def get_tag_nom(nomTag):
    return Tag.query.filter(Tag.nomTag == nomTag).first().idTag

def get_types():
    return TypeDocument.query.all()

def get_document_types(idTypeDoc, active_tags,filtre_texte):
    document = Document.query.filter(Document.idType == idTypeDoc).filter(Document.nomDoc.like('%' + filtre_texte + '%')).all()
    resultat = []
    if active_tags != []:
        for doc in document:
            est_present = True
            for tag in active_tags:
                if not DocumentTag.query.filter(DocumentTag.idTag == get_tag_nom(tag)).filter(DocumentTag.idDoc == doc.idDoc).all():
                    est_present = False
            if est_present:
                resultat.append(doc)
        return resultat 
    return document
def get_document_id(idDoc):
    return Document.query.get(idDoc)