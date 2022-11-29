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
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=100, verbose_name='title')),
                ('description', models.TextField(max_length=500, verbose_name='description')),
                ('type', models.CharField(choices=[('movie', 'movie_choice'), ('tv_show', 'tv_show_choice')], max_length=25, verbose_name='type')),
                ('creation_date', models.DateField(verbose_name='creation_date')),
                ('rating', models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='rating')),
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
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
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
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100, verbose_name='full_name')),
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
                ('role', models.TextField(null=True, verbose_name='role')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.person')),
            ],
            options={
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='filmworks',
            field=models.ManyToManyField(through='movies.PersonFilmwork', to='movies.Filmwork'),
        ),
        migrations.CreateModel(
            name='GenreFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
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
            field=models.ManyToManyField(through='movies.GenreFilmwork', to='movies.Filmwork'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.GenreFilmwork', to='movies.Genre', verbose_name='genres'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmwork', to='movies.Person', verbose_name='persons'),
        ),
    ]
