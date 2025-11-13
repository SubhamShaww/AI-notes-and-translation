from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from .utils import translate_text

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
    translated = translate_text(note.text, source_lang=note.language, target_lang=target_lang)
    if translated:
        note.translated_text = translated
        note.traslated_language = target_lang
        note.save()
        return Response({
            "original": {
                "text": note.text,
                "language": note.language
            },
            "translated": {
                "text": translated,
                "language": target_lang
            }
        })
    else:
        return Response({"error": "Translation failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)