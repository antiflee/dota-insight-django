# Generated by Django 2.0.1 on 2018-01-17 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('heroes', '0002_delete_hero'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('hero_id', models.CharField(max_length=10, unique=True)),
                ('imageUrl', models.URLField()),
            ],
        ),
    ]
