# Generated by Django 4.2.2 on 2023-07-06 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallet_api", "0003_rename_api_key_tiredperson_name_apikeytiredperson"),
    ]

    operations = [
        migrations.RenameField(
            model_name="apikeytiredperson",
            old_name="customer",
            new_name="name",
        ),
        migrations.RemoveField(
            model_name="tiredperson",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="tiredperson",
            name="is_active",
        ),
        migrations.AlterField(
            model_name="tiredperson",
            name="name",
            field=models.CharField(max_length=10, unique=True),
        ),
    ]