import django_filters
from django import forms
from django_filters import FilterSet
from django_filters import DateFilter
from .models import Post


class PostFilter(FilterSet):
    data = django_filters.DateFilter(field_name='data',
                                     widget=forms.DateInput(attrs={'type': 'date'}), label='Дата',
                                     lookup_expr='gt')
    class Meta:
       model = Post
       fields = {
           # поиск по названию
           'header': ['icontains'],
           # количество товаров должно быть больше или равно
           'author__user_author__username': ['exact'],



       }