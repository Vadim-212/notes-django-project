from django.urls import path, include
from . import views, views_api
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'note', views_api.NoteViewSet)
router.register(r'user', views_api.UserViewSet)


urlpatterns = [
        path('api/', include(router.urls)),
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


