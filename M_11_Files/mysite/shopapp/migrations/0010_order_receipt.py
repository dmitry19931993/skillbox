# Generated by Django 4.0.6 on 2023-07-20 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0009_merge_20230719_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='receipt',
            field=models.FileField(null=True, upload_to='orders/receipt/'),
        ),
    ]
