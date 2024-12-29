import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from chat.models import Salon, Message
from school.models import Classe
from chat.consumers import ChatConsumer
from django.urls import reverse
from forum.models import Sujet, Reponse


import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Learn.settings')
django.setup()


@pytest.mark.django_db
class TestChatConsumer:
    @pytest.fixture
    async def setup_data(self):
        """
        Prépare les données nécessaires pour les tests :
        - Crée un utilisateur, une classe, un salon, et un message.
        """
        user = await User.objects.create_user(username="testuser", password="password123")
        classe = await Classe.objects.create(nom="Math")
        salon = await Salon.objects.create(nom="Salon Math", classe=classe)
        message = await Message.objects.create(
            auteur=user, salon=salon, message="Bonjour tout le monde !"
        )
        return {"user": user, "classe": classe, "salon": salon, "message": message}

    async def test_fetch_messages(self, setup_data):
        """
        Teste la commande fetch_messages pour récupérer les messages d'un salon.
        """
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), f"/ws/instructor/messages/{setup_data['classe'].id}/")
        connected, _ = await communicator.connect()
        assert connected

        # Envoi de la commande fetch_messages
        await communicator.send_json_to({"command": "fetch_messages", "classe": setup_data['classe'].id})

        response = await communicator.receive_json_from()
        assert response["command"] == "messages"
        assert len(response["messages"]) == 1
        assert response["messages"][0]["message"] == "Bonjour tout le monde !"

        await communicator.disconnect()

    async def test_new_message(self, setup_data):
        """
        Teste la commande new_message pour l'ajout d'un nouveau message.
        """
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), f"/ws/instructor/messages/{setup_data['classe'].id}/")
        connected, _ = await communicator.connect()
        assert connected

        # Envoi d'un nouveau message
        await communicator.send_json_to({
            "command": "new_message",
            "from": setup_data['user'].username,
            "classe": setup_data['classe'].id,
            "message": "Nouveau message test !"
        })

        response = await communicator.receive_json_from()
        assert response["command"] == "new_message"
        assert response["message"]["message"] == "Nouveau message test !"

        await communicator.disconnect()

    async def test_chat_message_broadcast(self, setup_data):
        """
        Vérifie que le message est diffusé à tous les clients du salon.
        """
        communicator1 = WebsocketCommunicator(ChatConsumer.as_asgi(), f"/ws/instructor/messages/{setup_data['classe'].id}/")
        communicator2 = WebsocketCommunicator(ChatConsumer.as_asgi(), f"/ws/student/messages/{setup_data['classe'].id}/")

        # Connexion des deux clients
        connected1, _ = await communicator1.connect()
        connected2, _ = await communicator2.connect()
        assert connected1
        assert connected2

        # Client 1 envoie un message
        await communicator1.send_json_to({
            "command": "new_message",
            "from": setup_data['user'].username,
            "classe": setup_data['classe'].id,
            "message": "Message partagé !"
        })

        # Client 2 reçoit le message
        response = await communicator2.receive_json_from()
        assert response["message"]["message"] == "Message partagé !"

        await communicator1.disconnect()
        await communicator2.disconnect()
