from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from .services.telegram import send_telegram_message

@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if created:
        message = (
            f"💬 Новый комментарий\n\n"
            f"👤 Пользователь: {instance.user}\n"
            f"📝 Текст: {instance.text}"
        )
        send_telegram_message(message)

@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if created:
        if instance.status == "pending":
            send_telegram_message("📌 Новая заявка на модерацию...")