from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import *


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
