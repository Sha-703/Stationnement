# Generated by Django 5.2 on 2025-07-08 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0010_remove_pos_address_remove_pos_connection_type_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Produit',
            new_name='TypeEngin',
        ),
        migrations.RenameField(
            model_name='sale',
            old_name='produit',
            new_name='type_engin',
        ),
        migrations.RenameField(
            model_name='typeengin',
            old_name='nom_produit',
            new_name='nom_type_engin',
        ),
    ]
