# Generated by Django 3.1.10 on 2021-05-20 19:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wwwapp', '0074_workshop_short_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='max_points',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='qualification_threshold',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='workshopparticipant',
            name='qualification_result',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Liczba punktów'),
        ),
    ]