# Generated by Django 3.2.12 on 2022-02-13 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='evaluation',
            options={'ordering': ['id']},
        ),
    ]
