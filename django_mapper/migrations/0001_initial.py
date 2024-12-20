# Generated by Django 5.1.2 on 2024-10-25 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("uid", models.CharField(max_length=200)),
                ("store", models.CharField(max_length=200)),
                ("title", models.CharField(max_length=200)),
                ("url", models.CharField(max_length=200)),
                ("category", models.CharField(max_length=200)),
                ("description", models.TextField(default=None, null=True)),
                ("images", models.JSONField(default=list)),
                ("images_0", models.CharField(default=None, max_length=200, null=True)),
                ("images_1", models.CharField(default=None, max_length=200, null=True)),
                ("images_2", models.CharField(default=None, max_length=200, null=True)),
                ("images_3", models.CharField(default=None, max_length=200, null=True)),
                ("images_4", models.CharField(default=None, max_length=200, null=True)),
                ("images_5", models.CharField(default=None, max_length=200, null=True)),
                ("price", models.FloatField()),
                ("properties_as_text", models.CharField(max_length=200)),
                ("properties_as_dict", models.JSONField(null=True)),
                (
                    "properties_brand",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_label",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_country",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_color",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_material",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_mass_raw",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                ("properties_mass_num", models.FloatField(default=None, null=True)),
                (
                    "properties_mass_unit",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_volume_raw",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                ("properties_volume_num", models.FloatField(default=None, null=True)),
                (
                    "properties_volume_unit",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_dimensions_raw",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                ("properties_dimensions_d_list", models.JSONField(null=True)),
                (
                    "properties_dimensions_d_list_0",
                    models.FloatField(default=None, null=True),
                ),
                (
                    "properties_dimensions_d_list_1",
                    models.FloatField(default=None, null=True),
                ),
                (
                    "properties_dimensions_d_list_2",
                    models.FloatField(default=None, null=True),
                ),
                (
                    "properties_dimensions_d_list_3",
                    models.FloatField(default=None, null=True),
                ),
                (
                    "properties_dimensions_d_list_4",
                    models.FloatField(default=None, null=True),
                ),
                (
                    "properties_dimensions_d_list_5",
                    models.FloatField(default=None, null=True),
                ),
                (
                    "properties_dimensions_all_units_parsed",
                    models.BooleanField(default=None, null=True),
                ),
                ("properties_art_codes", models.JSONField(default=list)),
                (
                    "properties_art_codes_0",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_art_codes_1",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_art_codes_2",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_art_codes_3",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_art_codes_4",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_art_codes_5",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                ("properties_category_list_raw", models.JSONField(default=list)),
                (
                    "properties_category_list_raw_0",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_category_list_raw_1",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_category_list_raw_2",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_category_list_raw_3",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_category_list_raw_4",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                (
                    "properties_category_list_raw_5",
                    models.CharField(default=None, max_length=200, null=True),
                ),
            ],
        ),
    ]
