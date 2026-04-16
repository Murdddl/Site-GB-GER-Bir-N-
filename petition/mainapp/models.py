from django.db import models

class Signature(models.Model):
    name = models.CharField(max_length=100, blank=True, default='Anonym')
    signed = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending') # pending, approved

    def __str__(self):
        return f"{self.name} - {self.status}"
    
class Signature(models.Model):
    name = models.CharField(max_length=100, blank=True, default='Аноним')
    signed = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Question(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Auf Moderation'),
        ('approved', 'Erklaubt'),
        ('rejected', 'Nicht erlaubt'),
    ]
    question = models.TextField()
    answer = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.question[:50]
    
class Comment(models.Model):
    user = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

