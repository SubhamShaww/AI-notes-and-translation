from django.db import models

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    language = models.CharField(max_length=10)
    translated_text = models.TextField(blank=True, null=True)
    translated_language = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title