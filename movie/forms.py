from django import forms

from .models import Reviews


class ReviewFrom(forms.ModelForm):
    '''Форма отзыва'''
    class Meta:
        model = Reviews  # указываем, по какой модели делаем форму
        fields = ('name', 'email', 'text')  # указываем, какие поля мы хотим сделать
