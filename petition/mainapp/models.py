from django.db import models

class Signature(models.Model):
    name = models.CharField(max_length=100, blank=True, default='Аноним')
    signed = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    name = models.CharField(max_length=100, blank=True, default='Аноним')
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name