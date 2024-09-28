# Generated by Django 5.0.6 on 2024-09-27 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("landing", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactMessage",
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
                ("name", models.CharField(max_length=255)),
                ("mobile", models.CharField(max_length=12)),
                ("subject", models.CharField(max_length=255)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name="faq",
            options={"ordering": ["created_at"]},
        ),
        migrations.AlterField(
            model_name="faq",
            name="question",
            field=models.CharField(max_length=200, unique=True),
        ),
    ]