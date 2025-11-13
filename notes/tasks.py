from celery import shared_task
from .models import Note
from .utils import translate_text
from django.conf import settings

@shared_task
def async_translate_note(note_id, target_lang):
    try:
        note = Note.objects.get(id=note_id)
        translated = translate_text(note.text, source_lang=note.language, target_lang=target_lang)
        if translated:
            note.translated_text = translated
            note.traslated_language = target_lang
            note.save()

            # Cache result in Redis
            cache_key = f"translation:{note_id}:{target_lang}"
            # Cache for 1 hour
            settings.redis_client.set(cache_key, translated, ex=3600)  
            return True
        return False
    except Note.DoesNotExist:
        return False