# Generated by Django 4.1.1 on 2022-11-03 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wmtapp', '0002_remove_user_email_remove_user_password_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionIntolerance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intolerance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wmtapp.intolerance')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wmtapp.question')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wmtapp.category')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wmtapp.question')),
            ],
        ),
    ]
