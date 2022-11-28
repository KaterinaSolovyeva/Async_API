import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Roles(models.TextChoices):
    ACTOR = 'actor', _('actor')
    DIRECTOR = 'director', _('director')
    WRITER = 'writer', _('writer')


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.TextField(max_length=255, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    filmworks = models.ManyToManyField("Filmwork", through='GenreFilmwork')

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre_verbose_name')
        verbose_name_plural = _('genre_verbose_name_plural')

    def __str__(self):
        return self.name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('genre_filmwork_verbose_name')
        verbose_name_plural = _('genre_filmwork_verbose_name_plural')
        constraints = [
            UniqueConstraint(
                name='film_work_genre_idx',
                fields=['film_work', 'genre']
            )
        ]


class Filmwork(UUIDMixin, TimeStampedMixin):
    class MovieTypesChoices(models.TextChoices):
        MOVIE = 'movie', _('movie_choice')
        TVSHOW = 'tv_show', _('tv_show_choice')

    title = models.TextField(max_length=100, verbose_name=_('title'))
    description = models.TextField(max_length=500, verbose_name=_('description'))
    type = models.CharField(choices=MovieTypesChoices.choices, verbose_name=_('type'), max_length=25)
    creation_date = models.DateField(verbose_name=_('creation_date'))
    rating = models.FloatField(
        blank=True,
        verbose_name=_('rating'),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    genres = models.ManyToManyField("Genre", through='GenreFilmwork', verbose_name=_('genres'))
    persons = models.ManyToManyField("Person", through='PersonFilmwork', verbose_name=_('persons'))
    certificate = models.CharField(_('certificate'), max_length=512, blank=True, null=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('filmwork_verbose_name')
        verbose_name_plural = _('filmwork_verbose_name_plural')

    def __str__(self):
        return self.title


class Gender(models.TextChoices):
    MALE = 'male', _('male')
    FEMALE = 'female', _('female')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(max_length=100, verbose_name=_('full_name'))
    filmworks = models.ManyToManyField("Filmwork", through='PersonFilmwork')
    gender = models.TextField(_('gender'), choices=Gender.choices, null=True)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person_verbose_name')
        verbose_name_plural = _('person_verbose_name_plural')

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, related_name='filmwork_links')
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='person_links')
    role = models.TextField(null=True, verbose_name=_('role'), choices=Roles.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [
            UniqueConstraint(
                name='film_work_person_idx',
                fields=['film_work', 'person']
            )
        ]