from django.contrib import admin
from .models import Genre, GenreFilmwork, Filmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description', 'id')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    autocomplete_fields = ('persons', 'genres')
    list_display = ('title', 'type', 'creation_date', 'rating', 'get_genres')

    list_filter = ('type',)

    search_fields = ('title', 'description', 'id')

    list_prefetch_related = ('genres',)

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name', 'description')
