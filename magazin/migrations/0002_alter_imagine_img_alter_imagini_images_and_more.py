# Generated by Django 4.0 on 2022-02-10 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagine',
            name='img',
            field=models.FileField(null=True, upload_to='Products/', verbose_name='Card Image'),
        ),
        migrations.AlterField(
            model_name='imagini',
            name='images',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Imagini', to='magazin.imagine'),
        ),
        migrations.AlterField(
            model_name='produs',
            name='imagini',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Imagini', to='magazin.imagini'),
        ),
        migrations.AlterField(
            model_name='produs',
            name='specificatii',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Specificatii', to='magazin.specificatii'),
        ),
    ]