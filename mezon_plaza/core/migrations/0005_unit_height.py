# Generated by Django 4.2.19 on 2025-03-03 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_unit_tenant'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='height',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Высота (м)'),
            preserve_default=False,
        ),
    ]
