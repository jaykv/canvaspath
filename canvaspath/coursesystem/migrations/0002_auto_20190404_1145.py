# Generated by Django 2.1.7 on 2019-04-04 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursesystem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]
