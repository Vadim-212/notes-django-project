from django.urls import path, include
from . import views, views_api
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'note', views_api.NoteViewSet)
router.register(r'user', views_api.UserViewSet)


urlpatterns = [
        path('<int:note_id>', views.show_note, name='show_note'),
        path('add/', views.add_note),
        path('edit/<int:note_id>', views.edit_note),
        path('del/<int:note_id>', views.del_note),
        path('all/', views.show_user_notes, name='show_user_notes'),
        path('api/', include(router.urls)),
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


