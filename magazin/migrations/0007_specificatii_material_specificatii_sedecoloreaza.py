# Generated by Django 4.0 on 2022-02-12 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0006_produs_sters'),
    ]

    operations = [
        migrations.AddField(
            model_name='specificatii',
            name='material',
            field=models.CharField(default='In', max_length=20, verbose_name='Material'),
        ),
        migrations.AddField(
            model_name='specificatii',
            name='sedecoloreaza',
            field=models.BooleanField(default=False, verbose_name='Se decoloreaza'),
        ),
    ]
