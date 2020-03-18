from django.db import models
from django.db.models import fields as f
from django.urls import reverse

# Create your models here.


class User(models.Model):
    login = f.TextField()
    email = f.TextField()
    password = f.TextField()


class Note(models.Model):
    text = f.TextField()
    time_added = f.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = None

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('note-show', kwargs=dict(note_id=self.id))
