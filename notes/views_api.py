from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User
from . import serializers
from .models import Note


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-time_added')
    serializer_class = serializers.NoteSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]
