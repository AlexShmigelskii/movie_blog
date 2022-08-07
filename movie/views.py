from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import *
from .forms import ReviewFrom


class MovieView(ListView):
    '''Список фильмов'''
    model = Movie
    queryset = Movie.objects.filter(draft=False)  # не выводим те фильмы, которые помечены как "черновик"
    # template_name = 'movie/movie_list.html'
    # не указываем template_name т к Django автоматически ищет его под названием
    # '<название приложения>/movie_list.html' =  'movie/movie_list.html'


class MovieDetailView(DetailView):
    '''Полное описание фильма'''
    model = Movie
    slug_field = 'url'
    # template_name = 'movie/movie_detail.html'
    # не указываем template_name т к Django автоматически ищет его под названием
    # '<название приложения>/movie_detail.html' = 'movie/movie_detail.html'


class AddReview(View):
    '''Отзывы'''
    def post(self, request, pk):
        form = ReviewFrom(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)  # останавливаем сохранение нашей формы, чтобы внести изменения
            # form.movie_id = pk  # из таблицы movies_reviews взяли столбец, обозначенный как movie_id
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())
