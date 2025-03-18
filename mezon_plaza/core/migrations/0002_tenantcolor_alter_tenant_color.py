# Generated by Django 4.2.19 on 2025-03-02 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TenantColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=7, unique=True, verbose_name='Цвет (HEX)')),
            ],
            options={
                'verbose_name': 'Цвет арендатора',
                'verbose_name_plural': 'Цвета арендаторов',
            },
        ),
        migrations.AlterField(
            model_name='tenant',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.tenantcolor', verbose_name='Цвет арендатора'),
        ),
    ]
