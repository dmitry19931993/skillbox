# Generated by Django 4.0.6 on 2023-07-10 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0007_alter_product_options_product_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='user',
            new_name='created_by',
        ),
    ]
