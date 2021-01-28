# Generated by Django 3.1.4 on 2020-12-19 19:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('target_source', models.TextField(null=True)),
                ('target_type', models.TextField(null=True)),
                ('target_value', models.TextField(null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('creator_type', models.TextField(null=True)),
                ('creator_email', models.TextField(null=True)),
                ('creator_name', models.TextField(null=True)),
            ],
        ),
    ]