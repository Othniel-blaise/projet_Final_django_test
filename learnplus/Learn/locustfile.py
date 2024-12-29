from locust import HttpUser, task, between
from locust.runners import STATE_STOPPED

class DjangoAppUser(HttpUser):
    wait_time = between(1, 3)  # Attente entre chaque tâche simulée (en secondes)

    def on_start(self):
        """ Cette méthode est exécutée une fois lors de la connexion """
        self.login()

    def login(self):
        """ Se connecter à l'application en envoyant une requête POST """
        response = self.client.post("/login/", {"username": "testuser", "password": "password"})
        if response.status_code != 200:
            print("Échec de la connexion.")
        else:
            print("Connexion réussie.")

    @task(1)
    def view_dashboard(self):
        """ Accéder au tableau de bord après la connexion """
        self.client.get("/dashboard/")

    @task(2)
    def view_courses(self):
        """ Accéder à la liste des cours """
        self.client.get("/instructor/courses/")

    @task(3)
    def add_quiz(self):
        """ Ajouter un quiz """
        self.client.post("/instructor/quiz/add/", {
            "name": "Quiz test",
            "subject": "Math",
            "course": "Math 101"
        })
