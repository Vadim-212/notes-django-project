from rest_framework import serializers as s
from django.contrib.auth.models import User
from .models import Note


class NoteSerializer(s.ModelSerializer):
    class Meta:
        model = Note
        fields = ['url', 'text', 'user']


class UserSerializer(s.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff']
