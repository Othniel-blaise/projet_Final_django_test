from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from quiz.models import Subject, Quiz 
from school.models import Matiere, Cours,Niveau ,Classe,Chapitre
from forum.models import Sujet, Reponse 

# Test pour le dashboard de l'instructeur
class InstructorDashboardTestCase(TestCase):

    def setUp(self):
        # Créer un utilisateur pour le test
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password') 
    def test_dashboard_view(self):
        # Accéder à la page du dashboard
        response = self.client.get(reverse('dashboard'))
        # Vérifier que la page est rendue avec un code HTTP 200
        self.assertEqual(response.status_code, 200)
        # Vérifier que le nom de l'utilisateur est affiché dans le template
        self.assertContains(response, 'testuser')

# Test pour la gestion des cours de l'instructeur
class InstructorCoursesTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_courses_view(self):
        # Accéder à la page des cours
        response = self.client.get(reverse('instructor-courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instructor/courses.html') 
# Test pour l'ajout de cours par l'instructeur
class InstructorCourseAddTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_course_add_view(self):
        response = self.client.get(reverse('course-add'))
        self.assertEqual(response.status_code, 200)

    def test_post_course_add(self):
        data = {
            'name': 'New Course',
            'description': 'Description of new course',
        }
        response = self.client.post(reverse('course-add'), data)
        # Vérifier la redirection après ajout
        self.assertRedirects(response, reverse('instructor-courses'))
        # Vérifier que le cours a bien été ajouté
        self.assertTrue(Cours.objects.filter(name='New Course').exists())

# Test pour la gestion du forum de l'instructeur
class InstructorForumTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_forum_view(self):
        response = self.client.get(reverse('instructor-forum'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instructor/forum.html')  
# Test pour la suppression d'un chapitre
class InstructorDeleteChapitreTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        # Créer un chapitre pour les tests
        self.chapter = Chapter.objects.create(name='Chapter 1')

    def test_delete_chapitre(self):
        response = self.client.post(reverse('delete_chapitre'), {'chapter_id': self.chapter.id})
        self.assertEqual(response.status_code, 200)  # Vérifier la réponse AJAX
        # Vérifier que le chapitre a bien été supprimé
        self.assertFalse(Chapter.objects.filter(id=self.chapter.id).exists())

# Test pour la suppression d'une réponse
class InstructorAnswerDeleteTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        # Créer un sujet et une réponse pour les tests
        self.sujet = Sujet.objects.create(titre='Test Sujet', question='Test question', user=self.user)
        self.reponse = Reponse.objects.create(sujet=self.sujet, reponse='Test réponse', user=self.user)

    def test_answer_delete(self):
        response = self.client.post(reverse('answer_delete'), {'answer_id': self.reponse.id})
        self.assertEqual(response.status_code, 200) 
        self.assertFalse(Reponse.objects.filter(id=self.reponse.id).exists())

# Test pour l'ajout de quiz par l'instructeur
class InstructorQuizAddTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.subject = Subject.objects.create(name='Mathematics')
        self.classe = Classe.objects.create(name='Class A')
        self.cours = Cours.objects.create(name='Math 101')

    def test_quiz_add_view(self):
        response = self.client.get(reverse('instructor-quiz-add'))
        self.assertEqual(response.status_code, 200)

    def test_post_quiz_add(self):
        data = {
            'name': 'Math Quiz 1',
            'subject': self.subject.id,
            'classe': self.classe.id,
            'cours': self.cours.id
        }
        response = self.client.post(reverse('instructor-quiz-add'), data)
        self.assertRedirects(response, reverse('instructor-quizzes'))
        # Vérifier que le quiz a bien été ajouté
        self.assertTrue(Quiz.objects.filter(name='Math Quiz 1').exists())
