from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import mail_admins  # Функция для массовой отправки писем админам
from datetime import datetime
from .models import Appointment
from django.template.loader import render_to_string  # Если хотите использовать HTML-шаблон для письма

class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        # Создаем объект Appointment на основе данных из POST-запроса
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # Отправляем письмо всем админам.
        # Тема письма – имя клиента и дата записи (отформатированная)
        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        return redirect('appointments:make_appointment')
from django.shortcuts import render

# Create your views here.
