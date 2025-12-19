import random
from django.core.mail import send_mail
from django.utils import timezone

def send_verification_code(user):
    code = str(random.randint(100000, 999999))
    user.email_code = code
    user.code_created_at = timezone.now()
    user.save()

    send_mail(
        'Tasdiqlash kodi',
        f'Sizning tasdiqlash kodingiz: {code}\nKod 5 daqiqa amal qiladi.',
        'noreply@gmail.com',
        [user.email],
    )
