# Generated by Django 4.1.4 on 2023-01-03 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('group', models.CharField(blank=True, max_length=100, null=True)),
                ('filetype', models.CharField(choices=[('L', 'Local'), ('R', 'Remote')], default='L', max_length=1)),
                ('file', models.FileField(upload_to='files/')),
            ],
            options={
                'ordering': ['name', 'group'],
            },
        ),
    ]