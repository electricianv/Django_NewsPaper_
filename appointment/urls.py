from django.urls import path
from . import views

urlpatterns = [
    # Пример: маршрут для создания записи записи (appointment)
    path('make/', views.AppointmentView.as_view(), name='make_appointment'),
]
