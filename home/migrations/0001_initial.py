# Generated by Django 4.1.4 on 2023-01-05 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order', models.IntegerField(blank=True, default=0, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('page', models.CharField(blank=True, max_length=100, null=True)),
                ('filetype', models.CharField(choices=[('F', 'File'), ('U', 'URL')], default='L', max_length=1)),
                ('file', models.FileField(blank=True, null=True, upload_to='static/files/')),
                ('url', models.CharField(blank=True, default='', max_length=200, null=True)),
            ],
            options={
                'ordering': ['name', 'page'],
            },
        ),
    ]
