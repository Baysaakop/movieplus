# Generated by Django 4.0.5 on 2022-06-27 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_movie_genres_alter_movie_platforms_and_more'),
        ('users', '0006_customuser_movies_like_customuser_movies_watched_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='movies_like',
            field=models.ManyToManyField(blank=True, related_name='movies_like', to='movies.movie'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='movies_rated',
            field=models.ManyToManyField(blank=True, related_name='movies_rated', to='users.moviescore'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='movies_watched',
            field=models.ManyToManyField(blank=True, related_name='movies_watched', to='movies.movie'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='movies_watchlist',
            field=models.ManyToManyField(blank=True, related_name='movies_watchlist', to='movies.movie'),
        ),
    ]
