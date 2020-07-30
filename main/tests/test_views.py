
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.test.client import RequestFactory

from main import views
import main.models as m

# Create your tests here.


class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')
        self.assertContains(response, 'Thesis')

# Testons la vue indexDocs


class TestDocumentIndexViewPaginate(TestCase):

    ACTIVE_PAGINATION_HTML = """
        <li class="page-item active">
            <a href="{}?page={}" class="page-link">
            {}
            </a>
        </li>
    """

    def setUp(self):
        for n in range(15):
            m.create_document_test(n)

    def testFirstPage(self):
        # Test si la première page apparait dans la pagination

        url = reverse('main:indexDocs')
        #request = RequestFactory().get(path=url)
        #response = views.DocumentsIndexView.as_view()(request)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context_data['is_paginated'])
        self.assertInHTML(self.ACTIVE_PAGINATION_HTML.format(url, 1, 1),
                          response.rendered_content)


class TestDocumentIndexView(TestCase):
    def test_si_pas_de_documents(self):
        """Un message d'innexistance de documents doit apparaitre"""
        reponse = self.client.get(reverse('main:indexDocs'))
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, "Aucun Document n'est disponible.")
        self.assertQuerysetEqual(
            reponse.context['latest_document_list'], []
        )

    def test_si_vieux_document_abscent(self):
        """
            Un document Passé ne doit pas apparaitre"""
        # jours = models.LIMIT_DAYS + 1  # Il ya 8 jours
        doc = m.create_document_test(31)

        reponse = self.client.get(reverse('main:indexDocs'))
        self.assertNotContains(reponse, doc.titre_doc)

    def test_si_future_document_abscent(self):
        """
            Un document future ne doit pas
            apparaitre"""

        m.create_document_test(-2)

        reponse = self.client.get(reverse('main:indexDocs'))
        self.assertNotContains(reponse, "Essai34")


class TestDocumentDetailsView(TestCase):
    """
        Test si :
        test1: la page s'affiche normalement code 200
        test2: test si ce sont les bons détails qui s'affichent
        test3: S'assure qu'en saisissant un mauvais id on a la bonne réponse
    """

    # test1
    def test_si_page_details_document_recent(self):
        """test si on renvoie les bons détails"""
        doc = m.create_document_test(10)
        # doc = m.Document(titre_doc="Essai34")  # Document récent
        # créons l'url
        url = reverse('main:detailsDocs', args=(doc.pk,))
        reponse = self.client.get(url)
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, doc.titre_doc)

    def test_si_future_document_abscent(self):
        """ En entrant l'id d'un future document, un message d'erreur doit apparaitre
        """
        doc = m.create_document_test(-1)  # Document future
        # créons l'url
        url = reverse('main:detailsDocs', args=(doc.pk,))
        reponse = self.client.get(url)
        self.assertEqual(reponse.status_code, 404)
