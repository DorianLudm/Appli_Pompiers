CREATE TABLE DOCUMENT (
    idDoc int PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nomDoc VARCHAR(10) NOT NULL,
    fichierDoc VARCHAR(10) NOT NULL,
    idType int NOT NULL,
    FOREIGN KEY (idType) REFERENCES TYPE_DOCUMENT(idType)
);

CREATE TABLE TYPE_DOCUMENT(
    idType int PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nomType VARCHAR(10) NOT NULL
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
	idTag int NOT NULL,
	nomTag	VARCHAR(10) NOT NULL,
	niveauProtection int NOT NULL,
	couleurTag TEXT NOT NULL,
	PRIMARY KEY(idTag,niveauProtection),
	FOREIGN KEY(niveauProtection) REFERENCES CATEGORIE(idCat)
);

CREATE TABLE DOCUMENT_TAG(
    idDoc int NOT NULL,
    idTag int NOT NULL,
    PRIMARY KEY(idDoc, idTag),
    FOREIGN KEY (idDoc) REFERENCES DOCUMENT(idDoc),
    FOREIGN KEY (idTag) REFERENCES SOUS_CATEGORIE(idTag)
);

CREATE TABLE GRADE (
    idGrade int PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nomGrade VARCHAR(10) NOT NULL
);

CREATE TABLE ROLE(
    idRole int PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nomRole VARCHAR(10) NOT NULL
);

CREATE TABLE CASERNE(
    idCas int PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nomCaserne VARCHAR(10) NOT NULL,
    adresseCaserne VARCHAR(10) NOT NULL
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
    nomUtilisateur VARCHAR(10) NOT NULL,
    prenomUtilisateur VARCHAR(10) NOT NULL,
    identifiant VARCHAR(10) NOT NULL,
    mdp VARCHAR(10) NOT NULL,
    idGrade int NOT NULL,
    idRole int NOT NULL,
    idCas int NOT NULL,
    FOREIGN KEY (idGrade) REFERENCES GRADE(idGrade),
    FOREIGN KEY (idRole) REFERENCES ROLE(idRole),
    FOREIGN KEY (idCas) REFERENCES CASERNE(idCas)
);

