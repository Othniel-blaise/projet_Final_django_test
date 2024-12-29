from django.test import TestCase
from quiz.models import Subject

class SubjectTestCase(TestCase):

    def setUp(self):
        self.subject = Subject.objects.create(name='Mathematics', color='#ff5733')

    def test_subject_creation(self):
        # Vérifie que le nom et la couleur sont corrects
        self.assertEqual(self.subject.name, 'Mathematics')
        self.assertEqual(self.subject.color, '#ff5733')

    def test_get_html_badge(self):
        # Vérifie que la méthode get_html_badge renvoie le bon HTML
        html_badge = self.subject.get_html_badge()
        self.assertIn('<span class="badge badge-primary" style="background-color: #ff5733">Mathematics</span>', html_badge)
# 
from django.contrib.auth.models import User
from quiz.models import Quiz, Subject
from school.models import Classe, Cours

class QuizTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.subject = Subject.objects.create(name='Mathematics', color='#ff5733')
        self.classe = Classe.objects.create(name='Class A')  # Assure-toi d'avoir un modèle Classe valide
        self.cours = Cours.objects.create(name='Math 101')  # Assure-toi d'avoir un modèle Cours valide
        self.quiz = Quiz.objects.create(
            owner=self.user,
            name='Math Quiz 1',
            subject=self.subject,
            classe=self.classe,
            cours=self.cours
        )

    def test_quiz_creation(self):
        # Vérifie que le quiz a bien été créé avec les bonnes informations
        self.assertEqual(self.quiz.name, 'Math Quiz 1')
        self.assertEqual(self.quiz.subject.name, 'Mathematics')
        self.assertEqual(self.quiz.owner.username, 'testuser')

    def test_quiz_str(self):
        # Vérifie que la méthode __str__ renvoie le bon nom
        self.assertEqual(str(self.quiz), 'Math Quiz 1')
# 
from quiz.models import Question
from django.contrib.auth.models import User

class QuestionTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.subject = Subject.objects.create(name='Mathematics', color='#ff5733')
        self.classe = Classe.objects.create(name='Class A')
        self.cours = Cours.objects.create(name='Math 101')
        self.quiz = Quiz.objects.create(
            owner=self.user,
            name='Math Quiz 1',
            subject=self.subject,
            classe=self.classe,
            cours=self.cours
        )
        self.question = Question.objects.create(quiz=self.quiz, text='What is 2+2?')

    def test_question_creation(self):
        # Vérifie que la question a bien été créée
        self.assertEqual(self.question.text, 'What is 2+2?')

    def test_question_str(self):
        # Vérifie que la méthode __str__ renvoie le bon texte
        self.assertEqual(str(self.question), 'What is 2+2?')
# 
from quiz.models import Answer
from django.contrib.auth.models import User

class AnswerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.subject = Subject.objects.create(name='Mathematics', color='#ff5733')
        self.classe = Classe.objects.create(name='Class A')
        self.cours = Cours.objects.create(name='Math 101')
        self.quiz = Quiz.objects.create(
            owner=self.user,
            name='Math Quiz 1',
            subject=self.subject,
            classe=self.classe,
            cours=self.cours
        )
        self.question = Question.objects.create(quiz=self.quiz, text='What is 2+2?')
        self.answer = Answer.objects.create(question=self.question, text='4', is_correct=True)

    def test_answer_creation(self):
        # Vérifie que la réponse a bien été créée
        self.assertEqual(self.answer.text, '4')
        self.assertTrue(self.answer.is_correct)

    def test_answer_str(self):
        # Vérifie que la méthode __str__ renvoie la bonne réponse
        self.assertEqual(str(self.answer), '4')
# 
from quiz.models import TakenQuiz
from student.models import Student  # Assure-toi d'avoir un modèle Student valide

class TakenQuizTestCase(TestCase):

    def setUp(self):
        self.student = Student.objects.create(user=User.objects.create_user(username='studentuser', password='password'))
        self.subject = Subject.objects.create(name='Mathematics', color='#ff5733')
        self.classe = Classe.objects.create(name='Class A')
        self.cours = Cours.objects.create(name='Math 101')
        self.quiz = Quiz.objects.create(
            owner=self.student.user,
            name='Math Quiz 1',
            subject=self.subject,
            classe=self.classe,
            cours=self.cours
        )
        self.taken_quiz = TakenQuiz.objects.create(student=self.student, quiz=self.quiz, score=80, percentage=80.0)

    def test_taken_quiz_creation(self):
        # Vérifie que le quiz passé a bien été créé
        self.assertEqual(self.taken_quiz.score, 80)
        self.assertEqual(self.taken_quiz.percentage, 80.0)

    def test_taken_quiz_str(self):
        # Vérifie que la méthode __str__ renvoie la bonne chaîne
        self.assertEqual(str(self.taken_quiz), 'studentuser - Math Quiz 1')
# intégration
class TakeQuizTestCase(TestCase):

    def setUp(self):
        self.student = Student.objects.create(user=User.objects.create_user(username='studentuser', password='password'))
        self.subject = Subject.objects.create(name='Mathematics', color='#ff5733')
        self.classe = Classe.objects.create(name='Class A')
        self.cours = Cours.objects.create(name='Math 101')
        self.quiz = Quiz.objects.create(
            owner=self.student.user,
            name='Math Quiz 1',
            subject=self.subject,
            classe=self.classe,
            cours=self.cours
        )
        self.question = Question.objects.create(quiz=self.quiz, text='What is 2+2?')
        self.answer = Answer.objects.create(question=self.question, text='4', is_correct=True)

    def test_take_quiz(self):
        # Enregistrer une réponse d'un étudiant
        student_answer = StudentAnswer.objects.create(student=self.student, answer=self.answer)

        # Vérifier que l'étudiant a bien répondu
        self.assertEqual(student_answer.student.user.username, 'studentuser')
        self.assertEqual(student_answer.answer.text, '4')
