# Generated by Django 4.0.5 on 2022-10-01 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_episode_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='comments',
            field=models.ManyToManyField(blank=True, null=True, to='courses.comment'),
        ),
    ]
