from pdfminer.high_level import extract_text
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from unidecode import unidecode

nltk.download('punkt')
nltk.download('stopwords')

def generationTag(nom_file):

    text = extract_text('site_web/static/document/' + nom_file) # Ouvrir le fichier PDF et extraire le texte
    mot_brut = word_tokenize(text) # spliter le texte (le diviser en mots)
    mot_filtre = [] # Créer une liste vide pour stocker les mots filtrés
    for mot in mot_brut:
        mot = unidecode(mot)
        if mot not in stopwords.words('french') and mot not in string.punctuation and len(mot) > 2 :
            mot_filtre.append(mot.lower())
    frequence = Counter(mot_filtre) # Compte les fréquences de chaque mot
    mot_cles = frequence.most_common(10) # Obtient les 10 mots les plus fréquents
    print(transform(mot_cles))
    return mot_cles

def transform(mot_cles):
    liste_final = []
    for mot, val in mot_cles:
        string_mot = ""
        for char in mot:
            if char.isalpha():
                string_mot += char
        liste_final.append(string_mot)
    return liste_final


generationTag('SaeFestival.pdf')


