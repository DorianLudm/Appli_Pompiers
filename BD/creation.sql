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

CREATE TABLE GRADE (
    idGrade INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nomGrade VARCHAR(100) NOT NULL
);

CREATE TABLE ROLE(
    idRole INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nomRole VARCHAR(100) NOT NULL,
    niveauProtection int NOT NULL
);

CREATE TABLE CASERNE(
    idCas INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nomCaserne VARCHAR(255) NOT NULL,
    adresseCaserne VARCHAR(255) NOT NULL
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

CREATE TABLE FAVORIS(
    idUtilisateur int NOT NULL,
    idDoc int NOT NULL,
    PRIMARY KEY(idUtilisateur, idDoc),
    FOREIGN KEY (idUtilisateur) REFERENCES UTILISATEUR(idUtilisateur),
    FOREIGN KEY (idDoc) REFERENCES DOCUMENT(idDoc)
);
