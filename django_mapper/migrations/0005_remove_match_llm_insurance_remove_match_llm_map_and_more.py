# Generated by Django 5.1.2 on 2024-11-25 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "django_mapper",
            "0004_match_llm_insurance_match_llm_map_match_llm_raw_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="match",
            name="llm_insurance",
        ),
        migrations.RemoveField(
            model_name="match",
            name="llm_map",
        ),
        migrations.RemoveField(
            model_name="match",
            name="llm_raw",
        ),
        migrations.AlterField(
            model_name="match",
            name="insurance",
            field=models.FloatField(default=1.0),
        ),
        migrations.CreateModel(
            name="MatchLLM",
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
                ("llm_map", models.BooleanField(null=True)),
                ("llm_insurance", models.IntegerField(null=True)),
                ("llm_raw", models.CharField(max_length=20, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "product_1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_1_llm",
                        to="django_mapper.product",
                    ),
                ),
                (
                    "product_2",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_2_llm",
                        to="django_mapper.product",
                    ),
                ),
            ],
        ),
    ]