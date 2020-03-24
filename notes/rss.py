from django.contrib.syndication.views import Feed
from django.urls import reverse
from notes.models import Note


class LatestEntriesFeed(Feed):
    pass
