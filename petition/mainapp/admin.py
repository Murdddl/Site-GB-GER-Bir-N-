from django.contrib import admin
from .models import Signature, Review

@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'signed', 'date')
    list_filter = ('signed', 'date')
    search_fields = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'date')
    search_fields = ('name', 'text')
