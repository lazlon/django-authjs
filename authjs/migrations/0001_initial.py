# Generated by Django 5.1 on 2024-08-18 22:28

import django.contrib.sessions.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import authjs.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("sessions", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.CharField(default=authjs.models.generate_id, max_length=255, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=255, null=True, unique=True)),
                ("email_verified", models.DateTimeField(null=True)),
                ("image", models.CharField(max_length=255, null=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                ("session_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="sessions.session")),
                ("session_user", models.ForeignKey(db_column="user", on_delete=django.db.models.deletion.DO_NOTHING, to="authjs.user")),
            ],
            options={
                "verbose_name": "session",
                "verbose_name_plural": "sessions",
                "abstract": False,
            },
            bases=("sessions.session",),
            managers=[
                ("objects", django.contrib.sessions.models.SessionManager()),
            ],
        ),
        migrations.CreateModel(
            name="VerificationToken",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("identifier", models.CharField(max_length=255)),
                ("token", models.CharField(max_length=255, unique=True)),
                ("expires", models.DateTimeField()),
            ],
            options={
                "unique_together": {("identifier", "token")},
            },
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                ("id", models.CharField(default=authjs.models.generate_id, max_length=255, primary_key=True, serialize=False)),
                ("type", models.CharField(choices=[("oauth", "Oauth"), ("email", "Email"), ("credentials", "Credentials")], max_length=255)),
                ("provider", models.CharField(max_length=255)),
                ("provider_account_id", models.CharField(max_length=255)),
                ("refresh_token", models.TextField(null=True)),
                ("access_token", models.TextField(null=True)),
                ("expires_at", models.IntegerField(null=True)),
                ("token_type", models.CharField(max_length=255, null=True)),
                ("scope", models.CharField(max_length=255, null=True)),
                ("id_token", models.TextField(null=True)),
                ("session_state", models.CharField(max_length=255, null=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="authjs.user")),
            ],
            options={
                "unique_together": {("provider", "provider_account_id")},
            },
        ),
    ]
