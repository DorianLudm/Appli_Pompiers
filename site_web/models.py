from .app import db, login_manager
from flask_login import UserMixin, current_user
from sqlalchemy import func


class Caserne(db.Model):
    """caserne de pompiers"""
    idCas = db.Column(db.Integer, primary_key =True)
    nomCaserne = db.Column(db.String(100))
    adresseCaserne = db.Column(db.String(100))

    def get_id(self):
      return str(self.idCas)

class Grade(db.Model):
    """grade de pompier"""
    idGrade = db.Column(db.Integer, primary_key =True)
    nomGrade = db.Column(db.String(100))

    def get_id(self):   
        return str(self.idGrade)

class Role(db.Model):
    """classe représentant le rôle d'un utilisateur de l'application"""
    idRole = db.Column(db.Integer, primary_key =True)
    nomRole = db.Column(db.String(100))
    niveauProtection = db.Column(db.Integer)

    def get_id(self):
      return str(self.idRole)

class Utilisateur(db.Model, UserMixin):
    """classe représentant un utilisateur de l'application"""
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
    """type de document"""
    idType = db.Column(db.Integer, primary_key =True)
    nomType = db.Column(db.String(100))
    
class Document(db.Model):
    """classe réprésentant un document consultable dans l'application"""
    idDoc = db.Column(db.Integer, primary_key =True, autoincrement=True)
    nomDoc = db.Column(db.String(100))
    fichierDoc = db.Column(db.String(100))
    descriptionDoc = db.Column(db.String(500))
    niveauProtection = db.Column(db.Integer)
    idType = db.Column(db.Integer, db.ForeignKey('type_document.idType'))

    def __repr__(self) -> str:
        return f'Document {self.idDoc} : {self.nomDoc}'
    
class Tag(db.Model):
    """tag permettant la répertorisation des documents"""
    idTag = db.Column(db.Integer, primary_key =True, autoincrement=True)
    nomTag = db.Column(db.String(100))
    couleurTag = db.Column(db.String(100))

    def __hash__(self):
        return hash((self.idTag, self.nomTag, self.couleurTag))

    def __eq__(self, other):
        if isinstance(other, Tag):
            return self.idTag == other.idTag and self.nomTag == other.nomTag and self.couleurTag == other.couleurTag
        return False
    
class DocumentTag(db.Model):
    """classe représentant la relation entre les documents et leurs tags"""
    idTag = db.Column(db.Integer, db.ForeignKey('tag.idTag'), primary_key = True)
    idDoc = db.Column(db.Integer, db.ForeignKey('document.idDoc'), primary_key = True)
    index = db.Index('indexTag', idTag)

class Favoris(db.Model):
    """classe représentant la relation entre les utilisateurs et leurs documents favoris"""
    idUtilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.idUtilisateur'), primary_key = True)
    idDoc = db.Column(db.Integer, db.ForeignKey('document.idDoc'), primary_key = True)
    
def get_tags():
    """fonction d'obtention de tous les tags existants"""
    return Tag.query.order_by(Tag.nomTag).all()

def get_tag(nomTag, exact = False):
    """fonction d'obtention d'un tag à partir de son nom"""
    if nomTag is None:
        return None
    if exact:
        return Tag.query.filter(Tag.nomTag.ilike(nomTag)).first()
    return Tag.query.filter(Tag.nomTag.like('%' + nomTag + '%')).first()

def get_tags_nom(nomTag):
    """fonction d'obtention de tous les tags existants à partir d'un nom donné"""
    return Tag.query.filter(Tag.nomTag.ilike('%' + nomTag + '%')).all()

def get_tag_id(idTag):
    """fonction d'obtention d'un tag à partir de son id"""
    return Tag.query.get(idTag)

def get_tag_nom(nomTag):
    """fonction d'obtention de l'id d'un tag à partir de son nom"""
    return Tag.query.filter(Tag.nomTag == nomTag).first().idTag

def get_tag_idDoc(idDoc):
    """fonction d'obtention d'un document à partir de son id"""
    return DocumentTag.query.filter(DocumentTag.idDoc == idDoc).all()

def get_max_id_tag():
    """fonction renvoyant l'id de tag le plus élevé dans la BD"""
    max_id = db.session.query(db.func.max(Tag.idTag)).scalar()
    if max_id is None:
        return 0
    return max_id

def get_types():
    """fonction d'obtention des types des documents"""
    return TypeDocument.query.all()

def get_id_type(nomType):
    """fonction d'obtention de l'id d'un type à partir de son nom"""
    return TypeDocument.query.filter(TypeDocument.nomType == nomType).first().idType

def get_type(idType):
    """fonction d'obtention du nom d'un type à partir de son id"""
    return TypeDocument.query.filter(TypeDocument.idType == idType).first()

def get_documents():
    """fonction d'obtention de l'ensemble des documents existants"""
    role = Role.query.filter(Role.idRole == current_user.idRole).first()
    return Document.query.filter(Document.niveauProtection <= role.niveauProtection).all()

def get_max_id_document():
    """fonction d'obtention de l'id de document le plus élevé"""
    max_id = db.session.query(db.func.max(Document.idDoc)).scalar()
    if max_id is None:
        return 0
    return max_id

def get_document_types(idTypeDoc, document = []):
    """fonction de filtrage de documents à partir de leur type"""
    resultat = []
    for doc in document:
        if doc.idType == idTypeDoc:
            resultat.append(doc)
    return resultat 

def get_filtrer_document_tag(documents, tag):
    """fonction de filtrage de documents à partir d'un tag donné"""
    document_ids = set(document.idDoc for document in documents)
    
    result = DocumentTag.query.filter(
        DocumentTag.idTag == tag.idTag,
        DocumentTag.idDoc.in_(document_ids)
    ).all()
    resultat = [Document.query.get(doc.idDoc) for doc in result]
    return resultat

def get_filtrer_document_extension(documents, extension):
    """fonction de filtrage de documents à partir d'une extension donnée"""
    resultat = []
    for doc in documents:
        if doc.fichierDoc.lower().endswith(extension.lower()):
            resultat.append(doc)
    return resultat

def get_liaison_document_tag(idTag):
    """fonction d'obtention des liaisons entre un document et un tag pour tout les documents associés au tag"""
    return DocumentTag.query.filter(DocumentTag.idTag == idTag).all()

def get_filtrer_document_nom(documents, nom):
    """fonction de filtrage de documents à partir d'un nom donné"""
    resultat = []
    for doc in documents:
        if doc.nomDoc.lower().find(nom.lower()) != -1:
            resultat.append(doc)
    return resultat

def get_favoris_user(idUtilisateur):
    """fonction d'obtention des documents favoris d'un utilisateur"""
    role = Role.query.filter(Role.idRole == current_user.idRole).first()
    return Document.query.join(Favoris, Document.idDoc == Favoris.idDoc).filter(Favoris.idUtilisateur == idUtilisateur).filter(Document.niveauProtection <= role.niveauProtection).all()

def user_has_favoris(idUtilisateur, idDoc):
    """fonction de vérification de l'existence d'un document dans les favoris d'un utilisateur"""
    return Favoris.query.filter(Favoris.idUtilisateur == idUtilisateur).filter(Favoris.idDoc == idDoc).first()

def add_favoris(idUtilisateur, idDoc):
    """fonction d'ajout d'un document aux favoris d'un utilisateur"""
    favoris = Favoris(idUtilisateur = idUtilisateur, idDoc = idDoc)
    db.session.add(favoris)
    db.session.commit()

def remove_favoris(idUtilisateur, idDoc):
    """fonction de suppression d'un document des favoris d'un utilisateur"""
    favoris = Favoris.query.filter(Favoris.idUtilisateur == idUtilisateur).filter(Favoris.idDoc == idDoc).first()
    db.session.delete(favoris)
    db.session.commit()

def supprimer_doctag_by_docid(id):
    """Function to delete all DocumentTag instances based on the document's ID"""
    document_tags = DocumentTag.query.filter_by(idDoc=id).all()
    for document_tag in document_tags:
        db.session.delete(document_tag)
    db.session.commit()

def supprimer_favoris_by_docid(id):
    """fonction de suppression d'une instance de favoris selon l'id du document"""
    favoris = Favoris.query.filter_by(idDoc=id).all()
    for fav in favoris:
        db.session.delete(fav)
    db.session.commit()

def get_document_id(idDoc):
    """fonction d'obtention d'un document à partir de son id"""
    return Document.query.get(idDoc)
    
def get_utilisateurs():
    """fonction d'obtention de l'ensemble des utilisateurs"""
    return Utilisateur.query.order_by(func.upper(Utilisateur.nomUtilisateur), func.upper(Utilisateur.prenomUtilisateur)).all()

def is_identifant(identifant):
    """fonction de vérification de l'existence d'un identifiant dans la BD"""
    return Utilisateur.query.filter(Utilisateur.identifiant == identifant).first()

def is_admin_identifiant(identifant):
    """fonction de vérification de l'existence d'un identifiant dans la BD"""
    return Utilisateur.query.filter(Utilisateur.identifiant == identifant).filter(Utilisateur.idRole == -1).first()
    
def get_grades():
    """fonction d'obtention de l'ensemble des grades"""
    return Grade.query.all()

def get_roles():
    """fonction d'obtention de l'ensemble des roles"""
    return Role.query.all()

def get_utilisateur(idUtilisateur):
    """fonction d'obtention d'un utilisateur à partir d'un id donné"""
    return Utilisateur.query.get(idUtilisateur)

def get_nom_role(idRole):
    """fonction d'obtention d'un nom de rôle à partir d'un id donné"""
    return Role.query.filter_by(idRole=current_user.idRole).first().nomRole

def get_casernes():
    """fonction d'obtention de l'ensemble des casernes"""
    return Caserne.query.all()

def get_nom_grade(idGrade):
    """fonction d'obtention d'un nom de grade à partir de son id"""
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
    util['id'] = current_user.idUtilisateur
    util['nom'] = current_user.nomUtilisateur
    util['prenom'] = current_user.prenomUtilisateur
    util['grade'] = get_nom_grade(current_user.idGrade)
    util['role'] = get_nom_role(current_user.idRole)
    return util

def is_admin():
    infos = informations_utlisateurs()
    return "role" in infos.keys() and infos["role"] == 'Administrateur'