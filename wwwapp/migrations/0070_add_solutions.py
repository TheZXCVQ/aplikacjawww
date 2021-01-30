# Generated by Django 3.1.5 on 2021-01-29 21:33

from django.db import migrations, models
import django.db.models.deletion
import wwwapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0069_migrate_userinfo_to_wwwforms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_changed', models.DateTimeField(auto_now=True)),
                ('message', models.TextField(blank=True, help_text='Nie wpisuj rozwiązań w tym polu - załącz je jako plik. To pole jest przeznaczone jedynie na szybkie uwagi typu "poprawiłem plik X"', verbose_name='Komentarz dla prowadzącego')),
                ('workshop_participant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='solution', to='wwwapp.workshopparticipant')),
            ],
        ),
        migrations.AddField(
            model_name='workshop',
            name='solution_uploads_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='SolutionFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=wwwapp.models.solutions_dir, verbose_name='Plik')),
                ('last_changed', models.DateTimeField(auto_now=True)),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='wwwapp.solution')),
            ],
        ),
    ]
