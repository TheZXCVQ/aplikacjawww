# Generated by Django 3.1.7 on 2021-03-05 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0070_add_solutions'),
    ]

    operations = [
        migrations.AddField(
            model_name='solutionfile',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]