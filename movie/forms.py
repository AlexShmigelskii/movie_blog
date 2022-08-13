from django import forms

from .models import Reviews, Rating, RatingStar


class ReviewFrom(forms.ModelForm):
    '''Форма отзыва'''
    class Meta:
        model = Reviews  # указываем, по какой модели делаем форму
        fields = ('name', 'email', 'text')  # указываем, какие поля мы хотим сделать


class RatingForm(forms.ModelForm):
    '''Форма добавления рейтинга'''
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(),
        widget=forms.RadioSelect(),
        empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('star', )
