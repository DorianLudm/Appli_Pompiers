CREATE TABLE DOCUMENT (
    idDoc INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nomDoc VARCHAR(100) NOT NULL,
    fichierDoc VARCHAR(100) NOT NULL,
    idType int NOT NULL,
    descriptionDoc VARCHAR(500),
    niveauProtection int NOT NULL,
    FOREIGN KEY (idType) REFERENCES TYPE_DOCUMENT(idType)
);

CREATE TABLE TYPE_DOCUMENT(
    idType INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nomType VARCHAR(100) NOT NULL
);

CREATE TABLE ARCHIVE(
    idArchive int,
    dateRemplacement DATE NOT NULL,
    ancienPath VARCHAR NOT NULL,
    idDoc int NOT NULL,
    PRIMARY KEY(idArchive),
    FOREIGN KEY (idDoc) REFERENCES DOCUMENT(idDoc)
);

CREATE TABLE TAG (
	idTag int NOT NULL PRIMARY KEY,
	nomTag	VARCHAR(100) NOT NULL,
	couleurTag TEXT NOT NULL
);

CREATE TABLE DOCUMENT_TAG(
    idDoc int NOT NULL,
    idTag int NOT NULL,
    PRIMARY KEY(idDoc, idTag),
    FOREIGN KEY (idDoc) REFERENCES DOCUMENT(idDoc),
    FOREIGN KEY (idTag) REFERENCES TAG(idTag)
);

CREATE TABLE REPERTOIRE (
    idRep INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nomRepertoire VARCHAR(100) NOT NULL,
    tagAssocie int NOT NULL,
    FOREIGN KEY (tagAssocie) REFERENCES TAG(idTag)
);

CREATE TABLE GRADE (
    idGrade INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nomGrade VARCHAR(100) NOT NULL
);

CREATE TABLE ROLE(
    idRole INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    niveauProtection int NOT NULL,
    nomRole VARCHAR(100) NOT NULL
);

CREATE TABLE CASERNE(
    idCas INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nomCaserne VARCHAR(255) NOT NULL,
    adresseCaserne VARCHAR(255) NOT NULL
);

CREATE TABLE DIRIGER_CASERNE(
    idUtilisateur int NOT NULL,
    idCas int NOT NULL,
    PRIMARY KEY(idUtilisateur, idCas),
    FOREIGN KEY (idUtilisateur) REFERENCES UTILISATEUR(idUtilisateur),
    FOREIGN KEY (idCas) REFERENCES CASERNE(idCas)
);

CREATE TABLE UTILISATEUR(
    idUtilisateur int PRIMARY KEY NOT NULL,
    nomUtilisateur VARCHAR(100) NOT NULL,
    prenomUtilisateur VARCHAR(100) NOT NULL,
    identifiant VARCHAR(100) UNIQUE NOT NULL,
    mdp VARCHAR(100) NOT NULL,
    idGrade int NOT NULL,
    idRole int NOT NULL,
    idCas int NOT NULL,
    FOREIGN KEY (idGrade) REFERENCES GRADE(idGrade),
    FOREIGN KEY (idRole) REFERENCES ROLE(idRole),
    FOREIGN KEY (idCas) REFERENCES CASERNE(idCas)
);

CREATE TABLE RELATION_REPERTOIRE(
    idRepParent int NOT NULL,
    idRepEfant int NOT NULL,
    PRIMARY KEY(idRepParent, idRepEfant),
    FOREIGN KEY (idRepParent) REFERENCES REPERTOIRE(idRep),
    FOREIGN KEY (idRepEfant) REFERENCES REPERTOIRE(idRep)
);

CREATE TABLE LIAISON_REPERTOIRE_FICHIER(
    idRepParent int NOT NULL,
    idFicEnfant int UNIQUE NOT NULL,
    PRIMARY KEY(idRepParent, idFicEnfant),
    FOREIGN KEY (idRepParent) REFERENCES REPERTOIRE(idRep),
    FOREIGN KEY (idFicEnfant) REFERENCES DOCUMENT(idDoc)
);
