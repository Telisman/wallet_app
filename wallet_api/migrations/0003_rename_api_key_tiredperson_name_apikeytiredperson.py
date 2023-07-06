# Generated by Django 4.2.2 on 2023-07-06 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wallet_api", "0002_tiredperson"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tiredperson",
            old_name="api_key",
            new_name="name",
        ),
        migrations.CreateModel(
            name="APIKeyTiredPerson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key_api", models.CharField(max_length=64)),
                (
                    "customer",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wallet_api.tiredperson",
                    ),
                ),
            ],
        ),
    ]
