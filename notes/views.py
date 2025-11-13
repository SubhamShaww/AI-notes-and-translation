from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from .tasks import async_translate_note
from django.conf import settings
from django.db.models import Count

# Create your views here.
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-created_at')
    serializer_class = NoteSerializer

@api_view(['POST'])
def translate_note(request, note_id):
    target_lang = request.data.get('target_lang', 'hi')
    async_translate_note.delay(note_id, target_lang)
    return Response({
        "message": "Translation job submitted",
        "note_id": note_id,
        "target_language": target_lang
    }, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def get_translated_note(request, note_id):
    target_lang = request.query_params.get('lang', 'hi')
    cached_key = f"translation:{note_id}:{target_lang}"

    cached_translation = settings.redis_client.get(cached_key)
    if cached_translation:
        return Response({
            "note_id": note_id,
            "translated_text": cached_translation.decode('utf-8'),
            "language": target_lang,
            "cached": True
        })
    
    try:
        note = Note.objects.get(id=note_id)
        if note.traslated_language == target_lang:
            return Response({
                "note_id": note.id,
                "translated_text": note.translated_text,
                "language": target_lang,
                "cached": False
            })
        else:
            return Response({"message": "Translation not ready."}, status=status.HTTP_202_ACCEPTED)
    except Note.DoesNotExist:
        return Response({"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_stats(request):
    total_notes = Note.objects.count()
    translated_notes = Note.objects.exclude(translated_text__isnull=True).count()

    original_langs = Note.objects.values('language').annotate(count=Count('id'))
    translated_langs = Note.objects.values('translated_language').exclude(translated_language__isnull=True).annotate(count=Count('id'))

    return Response({
        "total_notes": total_notes,
        "translated_notes": translated_notes,
        "original_language_distribution": {entry['language']: entry['count'] for entry in original_langs},
        "translated_language_distribution": {entry['translated_language']: entry['count'] for entry in translated_langs}
    })