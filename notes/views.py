from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from .utils import translate_text
from django.conf import settings

# Create your views here.
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-created_at')
    serializer_class = NoteSerializer

@api_view(['POST'])
def translate_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return Response({"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND) 

    target_lang = request.data.get('target_lang', 'hi') # default to Hindi
    cached_key = f"translation:{note_id}:{target_lang}"

    # check Redis cache
    cached_translation = settings.redis_client.get(cached_key)
    if cached_translation:
        return Response({
            "original": {
                "text": note.text,
                "language": note.language
            },
            "translated": {
                "text": cached_translation.decode('utf-8'),
                "language": target_lang
            },
            "cached": True
        })

    # perform translation
    translated = translate_text(note.text, source_lang=note.language, target_lang=target_lang)
    if translated:
        note.translated_text = translated
        note.traslated_language = target_lang
        note.save()

        # store in Redis cache (with 1hr expiration)
        settings.redis_client.setex(cached_key, 3600, translated)

        return Response({
            "original": {
                "text": note.text,
                "language": note.language
            },
            "translated": {
                "text": translated,
                "language": target_lang
            },
            "cached": False
        })
    else:
        return Response({"error": "Translation failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)