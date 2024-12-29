from django.test import TestCase
from django.contrib.auth.models import User

from django.utils.text import slugify
from datetime import datetime
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Learn.settings')
django.setup()

class SujetTestCase(TestCase):
    
    def setUp(self):
        # Créer un utilisateur pour les tests
        self.user = User.objects.create_user(username='testuser', password='password')
        # Créer un sujet pour tester
        self.sujet = Sujet.objects.create(user=self.user, titre="Test Sujet", question="C'est une question ?", cours=None)

    def test_sujet_creation(self):
        # Vérifier si le sujet est correctement créé
        self.assertEqual(self.sujet.titre, "Test Sujet")
        self.assertTrue(self.sujet.slug.startswith(slugify(self.sujet.titre)))
        self.assertEqual(self.sujet.user.username, "testuser")

    def test_sujet_slug_generation(self):
        # Vérifier que le slug est bien généré lors de la sauvegarde
        slug = slugify(f"{self.sujet.titre}-{self.sujet.date_add}")
        self.assertEqual(self.sujet.slug, slug)
# ----------------------------------------------------------------
class ReponseTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.sujet = Sujet.objects.create(user=self.user, titre="Test Sujet", question="C'est une question ?", cours=None)
        self.reponse = Reponse.objects.create(user=self.user, sujet=self.sujet, reponse="C'est une réponse")

    def test_reponse_creation(self):
        # Vérifier que la réponse est correctement associée au sujet
        self.assertEqual(self.reponse.reponse, "C'est une réponse")
        self.assertEqual(self.reponse.sujet.titre, "Test Sujet")
        self.assertEqual(self.reponse.user.username, "testuser")
        
    def test_reponse_slug_generation(self):
        # Vérifier la génération du slug pour la réponse
        base_slug = slugify(self.reponse.sujet.titre)
        self.assertTrue(self.reponse.slug.startswith(base_slug))
# Tests d'intégration
from django.test import Client
from django.urls import reverse


class ForumViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.sujet1 = Sujet.objects.create(user=self.user, titre="Sujet 1", question="Question 1", cours=None)
        self.sujet2 = Sujet.objects.create(user=self.user, titre="Sujet 2", question="Question 2", cours=None)

    def test_forum_view_pagination(self):
        # Teste la pagination des sujets dans la vue forum
        response = self.client.get(reverse('forum'))
        self.assertEqual(response.status_code,)
        self.assertContains(response, "Sujet 1")
        self.assertContains(response, "Sujet 2")
        
    def test_forum_view_sujets(self):
        # Teste l'affichage des sujets dans la vue forum
        response = self.client.get(reverse('forum'))
        self.assertQuerysetEqual(response.context['forum_general'], ['<Sujet: Sujet 1>', '<Sujet: Sujet 2>'])
#  Tests fonctionnels
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from forum.models import Sujet, Reponse


class ForumFunctionalTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        
    def test_create_sujet_and_view_forum(self):
        # Connecter l'utilisateur
        self.client.login(username='testuser', password='password')
        
        # Créer un sujet via la vue (en supposant qu'il y ait une vue pour cela)
        response = self.client.post(reverse('create_sujet'), {
            'titre': 'Nouveau Sujet',
            'question': 'Quel est le meilleur framework Python ?',
            'cours': ''
        })
        self.assertEqual(response.status_code, 302)  # Redirection après création
        
        # Vérifier que le sujet est visible dans le forum
        response = self.client.get(reverse('forum'))
        self.assertContains(response, 'Nouveau Sujet')
        self.assertContains(response, 'Quel est le meilleur framework Python ?')
