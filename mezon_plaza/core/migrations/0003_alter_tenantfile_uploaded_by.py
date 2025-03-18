# Generated by Django 4.2.19 on 2025-03-02 01:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_tenantcolor_alter_tenant_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantfile',
            name='uploaded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Добавил'),
        ),
    ]
