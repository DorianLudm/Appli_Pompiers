import click
from .app import app, db
from .models import Utilisateur, max_id_utilisateur
from hashlib import sha256

@app.cli.command()
def initdb():
    """Crée la base de données """
    db.create_all()
    click.echo('Initialisation de la base de données')

@app.cli.command()
def newuser():
    """Crée un nouvel utilisateur """
    var_identifiant = input("Identifiant : ")
    var_mdp = sha256(input("Mot de passe : ").encode()).hexdigest()
    var_prenom = input("Prénom : ")
    var_nom = input("Nom : ")
    var_grade = input("Grade : ")
    var_role = input("Role : ")

    util = Utilisateur(
    idUtilisateur= max_id_utilisateur()+1,
    nomUtilisateur= var_nom,
    prenomUtilisateur= var_prenom,
    identifiant= var_identifiant,
    mdp= var_mdp,
    idGrade= var_grade,
    idRole= var_role,
    idCas= 1
    )
    db.session.add(util)
    db.session.commit()
    click.echo('Utilisateur créé')
