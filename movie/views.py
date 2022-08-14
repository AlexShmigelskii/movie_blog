from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie, Actor, Genre, Rating
from .forms import ReviewFrom, RatingForm


class GenreYear:
    '''Жанры и года выходов фильмов'''
    def get_genre(self):
        return Genre.objects.all()

    def get_year(self):
        return Movie.objects.filter(draft=False).values('year')


class MovieView(GenreYear, ListView):
    '''Список фильмов'''
    model = Movie
    queryset = Movie.objects.filter(draft=False)  # не выводим те фильмы, которые помечены как "черновик"
    # template_name = 'movie/movie_list.html'
    # не указываем template_name т к Django автоматически ищет его под названием
    # '<название приложения>/movie_list.html' =  'movie/movie_list.html'
    paginate_by = 2


class MovieDetailView(GenreYear, DetailView):
    '''Полное описание фильма'''
    model = Movie
    slug_field = 'url'
    # template_name = 'movie/movie_detail.html'
    # не указываем template_name т к Django автоматически ищет его под названием
    # '<название приложения>/movie_detail.html' = 'movie/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm
        return context


class AddReview(View):
    '''Отзывы'''
    def post(self, request, pk):
        form = ReviewFrom(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)  # останавливаем сохранение нашей формы, чтобы внести изменения
            # form.movie_id = pk  # из таблицы movies_reviews взяли столбец, обозначенный как movie_id
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    '''Вывод информации об актере'''
    model = Actor
    template_name = 'movie/actor.html'
    slug_field = 'name'


class FilterMovie(GenreYear, ListView):
    '''Фильтр фильмов'''
    paginate_by = 1

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |  # логическое ИЛИ
            Q(genre__in=self.request.GET.getlist('genre'))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('year')])
        context['genre'] = ''.join([f'genre={x}&' for x in self.request.GET.getlist('genre')])
        return context


class AddStarRating(View):
    '''Добавление рейтинга фильму'''
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    '''Поиск фильма'''
    paginate_by = 2

    def get_queryset(self):
        return Movie.objects.filter(title__iregex=self.request.GET.get('s'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['s'] = f's={self.request.GET.get("s")}&'
        return context
