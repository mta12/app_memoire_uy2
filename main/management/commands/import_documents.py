import csv
import os.path
import datetime

from django.core.management.base import BaseCommand
from collections import Counter

import main.models as m

# command: python3 manage.py import_documents main/fixtures/documents-samples.csv


def convertStringToDate(chaine):
    # Format de la chaine "jj/mm/aaaa"
    if len(chaine) != 0:
        liste_date = chaine.split('/')
        liste_date = [int(a) for a in liste_date]
        madate = datetime.date(
            liste_date[0], liste_date[1], liste_date[2])  # [jj, mm, aaaa]
        return madate
    else:
        return None


def extraireEnseignants(jurys, encadreurs):
    # les parametres sont des chaines
    # format de la chaine: Titre Nom | Titre Nom
    # retourne une liste de tuples (titre, role, nom)
    jury = 'JUR'
    encadreur = 'ENC'
    # jurys = (jurys.split('|'), jury)  # retour ([PR MANGA, PR TOBIE],1)
    enseignants = [(jurys.split('|'), jury),
                   (encadreurs.split('|'), encadreur)]
    liste_retour = []  # liste de tuples de chaines (titre, nom, role)
    for liste, role in enseignants:
        # print(liste, " ", role)
        for chaine in liste:
            chaine = chaine.strip()  # On enleve les espaces debut et fin
            # print(chaine)
            titre = chaine[:2]  # Les deux premiers elements
            # print(titre)
            nom = chaine[3:]  # A partir du troisieme element
            # print(nom, "\n")
            liste_retour.append((titre, nom, role))
    return liste_retour  # c un tuple de trois elts


def create_documents(count, row):
    # cré des documents
    p, created = m.Personne.objects.get_or_create(
        nom_complet=row['nom_etudiant'].strip())  # retourne un tuple (classe, bool)
    p.save()

    etud, created = m.Etudiant.objects.get_or_create(
        etudiant=p,
        matricule=row['matricule'].strip(),
    )
    etud.save()

    document, created = m.Document.objects.get_or_create(
        titre_doc=row['titre_doc'],
        auteur=etud,
    )
    document.save()
    if created:
        count["creee"] += 1
    # print("count {0}".format(count))

    document.type_doc = row['type_doc'].strip()
    # revoir pour les dates en testant la création des modèles
    # est ce qu'il faut convertir en Datetime???
    document.date_selection = convertStringToDate(
        row['date_selection'].strip())
    if row['est_soutenu'].strip().lower().__eq__('oui'):  # le document est soutenu
        document.est_soutenu = True
    else:
        document.est_soutenu = False
    document.date_soutenance = convertStringToDate(
        row['date_soutenance'].strip())
    document.note_soutenance = float(row['note_soutenance'].strip())
    document.etablissement = row['etablissement'].strip()
    document.type_formation = row['type_formation'].strip()
    document.filiere = row['filiere'].strip()
    document.resume_doc = row['resume_doc']

    # Ici aussi on doit gérer un FileField
    document.fichier = row['nom_fichier'].strip()

    # gestion des encadreurs et jurys
    jury_encadreurs = extraireEnseignants(
        row['jurys'], row['encadreurs'])
    for el in jury_encadreurs:
        p, created = m.Personne.objects.get_or_create(
            nom_complet=el[1])
        p.save()
        ens, created = m.Enseignant.objects.get_or_create(
            enseignant=p,
            titre_enseignant=el[0],
            role_enseignant=el[2],
        )
        ens.save()

        if created:
            # c["enseignants_created"] += 1
            if el[2] == 'JUR':
                document.jury.add(ens)
            else:  # ENC
                document.encadreur.add(ens)
        # else: raise an exception

    return count


class Command(BaseCommand):
    help = 'Import Documents in memoireuy2'
    # ./manage.py import_documents chemin_complet_fichier

    def add_arguments(self, parser):
        parser.add_argument("csv_file_name", type=str)
        # parser.add_argument("image_basedir", type=str)

    def handle(self, *args, **kwargs):
        self.stdout.write("Importing Documents")
        fichier = kwargs["csv_file_name"]
        c = Counter()
        c["docs"] = 0  # compte les documents
        c["creee"] = 0  # compte les documents créés

        with open(fichier, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                c["docs"] += 1
                # Traitement de chaque ligne
                # pers, created = m.Personne.objects.get_or_create(
                # nom_complet=row["nom_etudiant"].strip())
                print(row['encadreurs'], row['nom_etudiant'].strip(),
                      type(convertStringToDate(row['date_soutenance'])))

                c = create_documents(c, row)

        self.stdout.write(
            "Documents processed={1} (created={0})".format(c["creee"], c["docs"]))
