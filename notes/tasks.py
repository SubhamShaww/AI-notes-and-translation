from celery import shared_task
from .models import Note
from .utils import translate_text
from .redis_client import redis_client

@shared_task
def async_translate_note(note_id, target_lang):
    try:
        note = Note.objects.get(id=note_id)
        translated = translate_text(note.text, source_lang=note.language, target_lang=target_lang)
        print("Translated Text:", translated)
        if translated:
            note.translated_text = translated
            note.translated_language = target_lang
            note.save()

            # Cache result in Redis
            cache_key = f"translation:{note_id}:{target_lang}"
            # Cache for 1 hour
            redis_client.set(cache_key, translated, ex=3600)  
            return True
        return False
    except Note.DoesNotExist:
        return False