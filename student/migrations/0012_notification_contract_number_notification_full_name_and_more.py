# Generated by Django 4.2 on 2025-06-05 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_student_telegram_full_name_student_telegram_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='contract_number',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='full_name',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='phone_number',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
