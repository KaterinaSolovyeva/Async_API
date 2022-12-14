# Generated by Django 4.1.2 on 2022-12-02 09:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=100, verbose_name='title')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='description')),
                ('type', models.CharField(choices=[('movie', 'movie_choice'), ('tv_show', 'tv_show_choice')], max_length=25, verbose_name='type')),
                ('creation_date', models.DateField(blank=True, null=True, verbose_name='creation_date')),
                ('rating', models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='rating')),
                ('certificate', models.CharField(blank=True, max_length=512, null=True, verbose_name='certificate')),
                ('file_path', models.FileField(blank=True, null=True, upload_to='movies/', verbose_name='file')),
            ],
            options={
                'verbose_name': 'filmwork_verbose_name',
                'verbose_name_plural': 'filmwork_verbose_name_plural',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'genre_verbose_name',
                'verbose_name_plural': 'genre_verbose_name_plural',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100, verbose_name='full_name')),
                ('gender', models.TextField(choices=[('male', 'male'), ('female', 'female')], null=True, verbose_name='gender')),
            ],
            options={
                'verbose_name': 'person_verbose_name',
                'verbose_name_plural': 'person_verbose_name_plural',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.TextField(choices=[('actor', 'actor'), ('director', 'director'), ('writer', 'writer')], null=True, verbose_name='role')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filmwork_links', to='movies.filmwork')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_links', to='movies.person')),
            ],
            options={
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='filmworks',
            field=models.ManyToManyField(through='movies.PersonFilmwork', to='movies.filmwork'),
        ),
        migrations.CreateModel(
            name='GenreFilmwork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.genre')),
            ],
            options={
                'verbose_name': 'genre_filmwork_verbose_name',
                'verbose_name_plural': 'genre_filmwork_verbose_name_plural',
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.AddField(
            model_name='genre',
            name='filmworks',
            field=models.ManyToManyField(through='movies.GenreFilmwork', to='movies.filmwork'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.GenreFilmwork', to='movies.genre', verbose_name='genres'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmwork', to='movies.person', verbose_name='persons'),
        ),
        migrations.AddConstraint(
            model_name='personfilmwork',
            constraint=models.UniqueConstraint(fields=('film_work', 'person'), name='film_work_person_idx'),
        ),
        migrations.AddConstraint(
            model_name='genrefilmwork',
            constraint=models.UniqueConstraint(fields=('film_work', 'genre'), name='film_work_genre_idx'),
        ),
    ]
