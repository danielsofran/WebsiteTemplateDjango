# Generated by Django 4.0 on 2022-02-12 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0005_alter_imagine_colectie'),
    ]

    operations = [
        migrations.AddField(
            model_name='produs',
            name='sters',
            field=models.BooleanField(default=False, verbose_name='Sters'),
        ),
    ]
