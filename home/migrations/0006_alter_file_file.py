# Generated by Django 4.1.5 on 2023-01-31 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_sessioninfo_created_sessioninfo_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
    ]
