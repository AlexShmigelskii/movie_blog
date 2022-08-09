from django.contrib import admin

from .models import *


class ReviewInLine(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Категории'''
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    '''Фильмы'''
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [ReviewInLine]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    # fields = (('actors', 'directors', 'genre'), )
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'), )
        }),
        (None, {
            'fields': (('description', 'poster'),)
        }),
        (None, {
            'fields': (('year', 'world_premiere'),)
        }),
        (None, {
            'fields': (('country', 'budget'),)
        }),
        ('Actors', {
            'classes': ('collapse',),  # сворачивание
            'fields': (('directors', 'actors', 'genre'),)
        }),
        (None, {
            'fields': (('fees_usa', 'fees_world'),)
        }),
        (None, {
            'fields': (('category', 'url'), 'draft')
        }),

    )


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    '''Отзывы'''
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    '''Жанры'''
    list_display = ('name', 'url')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    '''Кадры из фильма'''
    list_display = ('title', 'movie', 'description')
    list_editable = ('description',)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    '''Актеры и режисеры'''
    list_display = ('name', 'age')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    '''Рейтинг'''
    list_display = ('ip', 'movie')


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    '''Звезда рейтинга'''
    list_display = ('value',)


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Genre)
# admin.site.register(Movie)
# admin.site.register(MovieShots)
# admin.site.register(Actor)
# admin.site.register(Rating)
# admin.site.register(RatingStar)
# admin.site.register(Reviews)
