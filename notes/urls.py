from django.urls import path, include
from rest_framework import DefaultRouter
from .views import NoteViewSet, translate_note, get_translated_note

router = DefaultRouter()
router.register(r'notes', NoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('translate/<int:note_id>/', translate_note),
    path('translated/<int:note_id>/', get_translated_note)
]