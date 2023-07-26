# Generated by Django 4.2.2 on 2023-06-30 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_alter_record_rating_alter_record_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(help_text='Enter File Description', verbose_name='File Description')),
                ('visible', models.BooleanField(default=True, help_text='Show this file on published record', verbose_name='File Visibility')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='records.record')),
            ],
            options={
                'ordering': ['-updated'],
            },
        ),
    ]
