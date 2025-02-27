# Generated by Django 5.1.4 on 2025-01-06 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DrugInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('manufacturer', models.CharField(blank=True, max_length=200, null=True)),
                ('active_ingredients', models.JSONField(blank=True, null=True)),
                ('dosage_form', models.CharField(blank=True, max_length=100, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'indexes': [models.Index(fields=['code'], name='api_druginf_code_0d7a52_idx')],
            },
        ),
    ]
