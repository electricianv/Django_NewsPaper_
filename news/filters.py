import django_filters
from django.forms.widgets import DateInput
from .models import Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title', lookup_expr='icontains', label='Название'
    )
    author__user__username = django_filters.CharFilter(
        field_name='author__user__username', lookup_expr='icontains', label='Имя автора'
    )
    date_created = django_filters.DateFilter(
        field_name='date_created',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
        label='Дата публикации после'
    )

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'date_created']
