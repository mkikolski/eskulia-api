"""
Moduł implementujący mockowy endpoint bota dla systemu czatu.

Moduł zawiera konfigurację połączenia z Firebase oraz endpoint API
symulujący odpowiedzi bota na wiadomości użytkownika. Wykorzystuje
Firestore do przechowywania historii konwersacji.
"""
from datetime import datetime

import firebase_admin
from django.shortcuts import render
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import ArrayUnion
from google.protobuf.internal.well_known_types import Timestamp
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from random import choice
from django.conf import settings

if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_CONFIG)
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

class MockBotEndpoint(APIView):
    """
    Endpoint API symulujący działanie chatbota.

    Klasa obsługuje żądania POST zawierające wiadomości użytkownika
    i generuje losowe odpowiedzi bota. Wszystkie wiadomości są zapisywane
    w bazie Firestore wraz z odpowiednimi metadanymi.

    Attributes:
        permission_classes (list): Lista klas uprawnień, ustawiona na [AllowAny]
            aby umożliwić dostęp wszystkim użytkownikom
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        doc_id = request.data.get('doc_id')
        user_msg = request.data.get('user_msg')

        if not doc_id or not user_msg:
            return Response({"error": "Missing doc_id or user_msg"}, status=status.HTTP_400_BAD_REQUEST)

        resp = choice([
            "She's an emotion avenger",
            "She is the villain who sends a",
            "Line of dark fantastic passion",
            "Words of love",
            "Words so leisured",
            "Words are poisoned darts of pleasure",
            "Die"
        ])

        _, msg_ref = db.collection(u'messages').add({"id": "", "message": user_msg, "sentByBot": False, "timestamp": datetime.utcnow()})
        db.collection(u'messages').document(msg_ref.id).update({"id": msg_ref.id})

        _, msg_ref_bot = db.collection(u'messages').add(
            {"id": "", "message": resp, "sentByBot": True, "timestamp": datetime.utcnow()})
        db.collection(u'messages').document(msg_ref_bot.id).update({"id": msg_ref_bot.id})

        db.collection(u'chats').document(doc_id).update({"chatMessagesIds": ArrayUnion([msg_ref.id, msg_ref_bot.id]), "lastMessage": resp})

        return Response(status=status.HTTP_200_OK)
