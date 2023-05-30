# Generated by Django 4.1 on 2023-05-27 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_destination'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.FileField(upload_to='images')),
            ],
        ),
        migrations.RemoveField(
            model_name='destination',
            name='image',
        ),
        migrations.AddField(
            model_name='destination',
            name='image',
            field=models.ManyToManyField(to='myapp.image'),
        ),
    ]
