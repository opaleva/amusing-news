# Generated by Django 3.2.8 on 2021-12-02 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20211130_1754'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='body',
            new_name='content',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
