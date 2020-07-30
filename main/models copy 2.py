import datetime

from django import forms
from django.db import models
from django.utils import timezone
from django.db.models import Q

# LIMIT_DAYS = 366  # Nombre de jours à ne pas dépasser pour un document passé

# Create your models here.

# Fields CHOICES: P86
# obj.get_att_display pour avoir les bonnes valeurs

# Nb de jours limites pour qu'un document soit considéré comme vieux
LIMIT_DAYS = 30


class Personne(models.Model):
    nom_complet = models.CharField(max_length=60)

    class Meta:
        ordering = (
            'nom_complet',
        )

    def __str__(self):
        return f"{self.nom_complet}"


class Enseignant(models.Model):
    jur, enc = 'JUR', 'ENC'
    ROLE_CHOICES = [
        (jur, 'Membre du Jury'),
        (enc, 'Encadreur'),
    ]
    ass, cc, mc, pr = 'ASS', 'CC', 'MC', 'PR'
    TITLE_CHOICES = [
        (ass, 'Assistant'),
        (cc, 'Chargé de cours'),
        (mc, 'Maitre de Conférence'),
        (pr, 'Professeur'),
    ]

    enseignant = models.ForeignKey(Personne, on_delete=models.CASCADE)
    titre_enseignant = models.CharField(max_length=3, choices=TITLE_CHOICES)
    role_enseignant = models.CharField(max_length=3, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.titre_enseignant} {self.enseignant} ({self.role_enseignant})"


class Etudiant(models.Model):
    etudiant = models.ForeignKey(Personne, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.etudiant}"


class DocumentQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            search_lookup = (Q(title__icontains=query) |
                             Q(type_doc__icontains=query))

            qs = qs.filter(search_lookup).distinct()
        return qs


class DocumentManager(models.Manager):
    def get_queryset(self):
        return DocumentQuerySet(self.model, using=self._db)


class Document(models.Model):
    # workflow des états du document: en cours, soutenu, archivé
    """ Les fields: P252
    Pour ce modèle, Un document est une these ou un mémoire
    on pourra l'étenre à autre chose plus tard
    """

    # On ordone l'affichage des documents
    class Meta:
        ordering = (
            '-date_soutenance', 'titre_doc'
        )

    fsjp = 'FSJP'
    fseg = 'FSEG'
    ETABLISSEMENT_CHOICES = [
        (fsjp, 'Faculté des Sciences Juridiques et Politiques'),
        (fseg, 'Faculté des Sciences Economiques et de Gestion'),
    ]
    master = 'MAS'
    doctorat = 'DOC'
    TYPE_DIPLOMES = [
        (master, 'Mémoire de Master'),
        (doctorat, 'Thèse de Doctorat'),
    ]
    acca = 'ACC'
    pro = 'PRO'
    TYPE_FORMATION = [
        (acca, 'Formation Académique'),
        (pro, 'Formation professionnelle'),
    ]

    type_doc = models.CharField(
        max_length=3, choices=TYPE_DIPLOMES, default=master, null=True)
    titre_doc = models.CharField(max_length=50, null=False)
    resume_doc = models.TextField(null=True)
    date_selection = models.DateField(
        'Date de Selection', null=True, blank=True)

    pub_date = models.DateTimeField(
        'Date de Publication ', null=True, default=timezone.now)
    est_soutenu = models.BooleanField(default=False)
    date_soutenance = models.DateField(
        'Date de Soutenance', null=True, blank=True)
    note_soutenance = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True)
    # Pour définir l'heure actuelle on peut utiliser django.utils.timezone.now()

    auteur = models.ForeignKey(Etudiant, on_delete=models.CASCADE)

    etablissement = models.CharField(
        max_length=6, choices=ETABLISSEMENT_CHOICES, default=fseg, null=True)
    type_formation = models.CharField(
        max_length=3, choices=TYPE_FORMATION, default=acca, null=True)
    filiere = models.CharField(max_length=20, null=True)

    jury = models.ManyToManyField(Enseignant, related_name="jury")
    encadreur = models.ManyToManyField(Enseignant, related_name="encadreur")

    # code_doc_pdf= models.CharField(max_length=10) #Le nom du fichier sera son id
    # doc.fichier == None teste si le fichier existe
    fichier = models.FileField(upload_to='uploads/docs', null=True, blank=True)

    # Un Manager specifique pour ce modele
    objects = DocumentManager()

    # ---------- Les fonctions du modèle DOcumens

    def __str__(self):
        return f"{self.type_doc} de {self.auteur}, titre: {self.titre_doc}"

    def est_document_recent(self):
        """
        Renvoie True si le document fut publié récemments
        Ecrire un test pour ça
        pub_date doit être dans la plage de moins de 24h
        """
        now = timezone.now()
        il_ya_nb_j = now - datetime.timedelta(days=LIMIT_DAYS)
        # return il_ya_nb_j <= self.pub_date <= now
        # On se limite à la date actuelle
        return il_ya_nb_j <= self.pub_date <= now


def create_document_test(jours):
    # temps = timezone.now() - datetime.timedelta(20)
    # cette methode marche aussi au niveau du shell
    pers = Personne(nom_complet=f"MTA23 {jours}")
    pers.save()
    etud = Etudiant(etudiant=pers, matricule=f"ZZZ {jours}")
    etud.save()
    ens = Enseignant(enseignant=pers)
    ens.save()

    doc = Document.objects.create(
        titre_doc=f"Debut du mouvement {jours}",
        pub_date=timezone.now() - datetime.timedelta(days=jours),
        auteur=etud,
    )
    doc.save()
    doc.encadreur.add(ens)
    doc.jury.add(ens)
    doc.save()
    return doc


def recherche_avec_liste_elements(cles):
    """
    retourne une liste de résultats pour chaque elements de la liste initiale
    """
    liste_retour = []
    if len(cles) != 0:
        for q in cles:
            l = m.Document.objects.filter(
                titre_doc__icontains=q).distinct()
            liste_retour.append(l)
    return liste_retour
