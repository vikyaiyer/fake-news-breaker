# Generated by Django 2.0.3 on 2018-03-25 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bsearch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchhistory',
            name='result',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='searchhistory',
            name='queries',
            field=models.CharField(max_length=2000),
        ),
    ]