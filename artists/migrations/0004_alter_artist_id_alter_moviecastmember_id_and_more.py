# Generated by Django 4.0.5 on 2022-07-01 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0003_auto_20220701_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='moviecastmember',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='moviecrewmember',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
