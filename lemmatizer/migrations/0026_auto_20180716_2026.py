# Generated by Django 2.0.6 on 2018-07-16 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatizer', '0025_auto_20180716_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formatlemmatizedtext',
            name='question',
            field=models.CharField(default='IX - II = ', max_length=17),
        ),
        migrations.AlterField(
            model_name='lemmmatizer',
            name='question',
            field=models.CharField(default='II + IX = ', max_length=15),
        ),
    ]
