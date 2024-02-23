# Appli_Pompiers

Application demandé par le SDIS 45

## Membres
- Ludmann Dorian
- Massuard Charles
- Haudebourg Baptiste
- Chidlovsky Léopold
- Demaret Sullivan

## Fonctionnalités
Pompier:
- Recherche de document
- Filtrer la recherche par plusieurs options (extension, nom, tags)
- Favoriser un document
- Visualiser un document
- Télécharger un document

Administrateur:
- Gérer (ajouter, modifier et supprimer) les comptes
- Gérer les documents
- Gérer les tags
- Rechercher les documents (mêmes options qu'utilisateur)

Autres:
- Système de niveau de protection

## Utilisation de l'application
Pour lancer l'application, vous devez avoir python et pip d'installés
Ouvrez votre terminal et entrer la commande suivante:
```bash
pip install -r requirements.txt
```

Ensuite, lancez l'application avec
```py
flask run
```