from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

class MyAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        """
        Переопределяем отправку письма подтверждения регистрации.
        В теме письма будет заголовок (можно изменить на любое другое значение),
        а в теле письма приветствие с именем пользователя и активационная ссылка.
        """
        print("Отправка письма подтверждения для:", emailconfirmation.email_address.email)
        activation_url = self.get_email_confirmation_url(request, emailconfirmation)
        user = emailconfirmation.email_address.user
        ctx = {
            "user": user,
            "activation_url": activation_url,
        }
        subject = f"Добро пожаловать, {user.username}!"  # Тема письма — имя пользователя
        message = render_to_string("emails/email_confirmation_message.txt", ctx)
        html_message = render_to_string("emails/email_confirmation_message.html", ctx)

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[emailconfirmation.email_address.email],
            html_message=html_message,
        )
