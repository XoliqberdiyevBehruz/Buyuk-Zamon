import requests
from celery import shared_task

from apps.student import models, utils


@shared_task
def send_telegram_message(token, id, text):
    try:
        student = models.Student.objects.get(id=id)
    except models.Student.DoesNotExist:
        return {"student not found"}
    
    if student.telegram_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": student.telegram_id,
            "text": utils.format_text(text, student),
        }
        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            return {"status": "success", "response": response.json()}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}
    return {"status": "error", "message": "Telegram ID not set for student"}