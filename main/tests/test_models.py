import tempfile
import datetime

from io import StringIO
from django.conf import settings
from django.test import TestCase, override_settings
from django.core.management import call_command
from django.utils import timezone

#from main.models import Document, Personne, Enseignant, Etudiant
import main.models as m
#from main import models

# Create your tests here.

# Une classe par modèle

"""
    - On ne peux pas créer un document dans le future 
    - On ne peut créer un document qui est soutenu mais n'a pas de date et vice versa
"""


class TestDocumentModels(TestCase):
    """
    Les futures publications ne doivent pas être considérées comme récentes
    Les publication de plus d'un jour aussi
    Les publications de 1 jour au plus sont récentes
    """

    def test_si_future_document_est_recent(self):
        """
        Doit retourner False pour un document à publier dans le future
        """
        # On se posititionne dans le future
        future = timezone.now() + datetime.timedelta(days=1)
        # On cré un document à publier dans le future
        doc = m.Document(pub_date=future)
        self.assertIs(doc.est_document_recent(), False)

    def test_si_vieux_document_est_recent(self):
        """
        Doit retourner False car un vieux document (publié avant la limit_day)
        """
        past = timezone.now() - datetime.timedelta(days=m.LIMIT_DAYS, seconds=1)
        doc = m.Document(pub_date=past)
        self.assertIs(doc.est_document_recent(), False)

    def test_si_actuel_document_est_recent(self):
        """
        Doit retourner True
        """
        # On se posititionne dans la plage de 24h
        now = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        # On cré un document à publier
        doc = m.Document(pub_date=now)
        self.assertIs(doc.est_document_recent(), True)

    def test_creation_document(self):
        """Test si le document se cré normalement"""
        doc = m.create_document_test(0)
        #d = Document.objects.filter(document_titre_doc__)
        self.assertIn(doc, m.Document.objects.all())


class TestImportDoc(TestCase):
    # ./manage.py test tests.test_models.TestImportDoc
    """ 
    The test asserts that the stdout is equal to what is expected, 
    and the number of models present after the import is what it should be
    """
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())  # dossier temporaire des fichiers
    def test_import_documents(self):
        out = StringIO()

        args = ['main/fixtures/documents-samples.csv', ]

        call_command('import_documents', *args, stdout=out)
        expected_out = ("Importing Documents\n"
                        "Documents processed=4 (created=4)\n"
                        )
        self.assertIn(out.getvalue(), expected_out)
        self.assertEqual(m.Document.objects.count(), 4)
