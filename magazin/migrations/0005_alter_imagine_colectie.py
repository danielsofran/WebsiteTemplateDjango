# Generated by Django 4.0 on 2022-02-10 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('magazin', '0004_alter_pret_reducere_alter_rating_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagine',
            name='colectie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ColectieImagini', to='magazin.imagini'),
        ),
    ]