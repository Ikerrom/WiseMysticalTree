# Generated by Django 4.1.1 on 2022-11-10 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wmtapp', '0004_categorygroup_categorygroupcategory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='preference',
            field=models.BooleanField(default=False),
        ),
    ]
