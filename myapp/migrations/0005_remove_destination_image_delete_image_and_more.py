# Generated by Django 4.1 on 2023-05-28 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_package'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination',
            name='image',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AddField(
            model_name='destination',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='destinations'),
        ),
    ]
