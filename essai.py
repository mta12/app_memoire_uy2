import datetime


def convertStringToDate(chaine):
    # Format de la chaine "jj/mm/aaaa"
    liste_date = chaine.split('/')
    liste_date = [int(a) for a in liste_date]
    madate = datetime.date(liste_date[2], liste_date[1], liste_date[0])
    return madate

    # prend une chaine et s'assure quelle ne commence pas par un vide
    # PB ON VEUT ELIMINER LES ESPACES AU DEBUT ET A LA FIN chaine.strip()


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


if __name__ == '__main__':
    # s = convertStringToDate("09/06/2020")
    # print(f"type de s {type(s)}, valeur de s {s}")
    #s = extraireEnseignants(" PR Manga Tob | PR Akono ", " PR Towa Jean")
    # print(s)
    jury_encadreurs = extraireEnseignants(
        "PR Manga Tob | PR Akono", "PR Towa Jean")
    print(jury_encadreurs)
    for el in jury_encadreurs:
        print(len(el))
        print(
            f"titre_enseignant= {el[0]}, nom= {el[1]}, role= {el[2]}, {type(el[1])}")
