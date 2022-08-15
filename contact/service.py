from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Вы подписались на рассылку',
        'Теперь вы будете получать от нас много спама',
        'DJANGO5003626@gmail.com',
        [user_email],
        fail_silently=False,
    )
