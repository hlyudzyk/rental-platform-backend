# Generated by Django 5.0.7 on 2024-08-22 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0002_user_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(null=True, upload_to='uploads/avatars'),
        ),
    ]
