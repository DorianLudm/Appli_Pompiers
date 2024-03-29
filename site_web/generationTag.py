from pdfminer.high_level import extract_text
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from unidecode import unidecode
from .models import Tag, get_max_id_tag
import random
from .app import app, mkpath, db


nltk.download('punkt')
nltk.download('stopwords')

def generationTag(nom_file):

    text = extract_text(nom_file) # Ouvrir le fichier PDF et extraire le texte
    mot_brut = word_tokenize(text) # spliter le texte (le diviser en mots)
    mot_filtre = [] # Créer une liste vide pour stocker les mots filtrés
    for mot in mot_brut:
        mot = unidecode(mot)
        if mot not in stopwords.words('french') and mot not in string.punctuation and len(mot) > 2 :
            mot_filtre.append(mot.lower())
    frequence = Counter(mot_filtre) # Compte les fréquences de chaque mot
    mot_cles = frequence.most_common(10) # Obtient les 10 mots les plus fréquents
    mot_cles = transform_tag(transform(mot_cles))
    return set(mot_cles)

def transform(mot_cles):
    liste_final = []
    for mot, val in mot_cles:
        string_mot = ""
        for char in mot:
            if char.isalpha():
                string_mot += char
        liste_final.append(string_mot)
    return liste_final

def transform_tag(mot_cles):
    liste_tag = []
    idMax = get_max_id_tag()
    for mot in mot_cles:
        mot = mot[0].upper() + mot[1:] # Mettre la première lettre en majuscule
        tagExist = Tag.query.filter(Tag.nomTag == mot).first()
        if not tagExist:
            a = hex(random.randrange(100,256))
            b = hex(random.randrange(100,256))
            c = hex(random.randrange(100,256))
            idMax += 1
            tag = Tag(
                idTag = idMax,
                nomTag = mot,
                couleurTag = a[2:]+b[2:]+c[2:]
            )
            liste_tag.append(tag)
        else:
            liste_tag.append(tagExist)
    return liste_tag



def generationTagDossier(nom_file):
    if not nom_file.endswith('.pdf'):
        return set()
    text = extract_text(nom_file) # Ouvrir le fichier PDF et extraire le texte
    mot_brut = word_tokenize(text) # spliter le texte (le diviser en mots)
    mot_filtre = [] # Créer une liste vide pour stocker les mots filtrés
    for mot in mot_brut:
        mot = unidecode(mot)
        if mot not in stopwords.words('french') and mot not in string.punctuation and len(mot) > 2 :
            mot_filtre.append(mot.lower())
    frequence = Counter(mot_filtre) # Compte les fréquences de chaque mot
    mot_cles = frequence.most_common(10) # Obtient les 10 mots les plus fréquents
    mot_cles = transform_tag_dossier(transform(mot_cles))
    return set(mot_cles) if mot_cles is not None else set()


def transform_tag_dossier(mot_cles):
    liste_tag = []
    print(mot_cles)
    for mot in mot_cles:
        if mot:
            mot = mot[0].upper() + mot[1:] # Mettre la première lettre en majuscule
            tagExist = Tag.query.filter(Tag.nomTag == mot).first()
            if not tagExist:
                a = hex(random.randrange(100,256))
                b = hex(random.randrange(100,256))
                c = hex(random.randrange(100,256))
                tag = Tag(
                    idTag = get_max_id_tag() + 1,   
                    nomTag = mot,
                    couleurTag = a[2:]+b[2:]+c[2:]
                )
                liste_tag.append(tag)
                db.session.add(tag)
                db.session.commit()
            else:
                liste_tag.append(tagExist)
        return liste_tag




