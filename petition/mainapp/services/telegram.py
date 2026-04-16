import requests
from django.conf import settings
import threading


def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Telegram error: {e}")
        return None


def async_send(text: str):
    thread = threading.Thread(
        target=send_telegram_message,
        args=(text,),
        daemon=True
    )
    thread.start()