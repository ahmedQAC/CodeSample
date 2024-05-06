# Generated by Django 4.2.6 on 2023-10-23 13:23

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('invitation_uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('private_session', models.BooleanField(default=True)),
                ('amount_per_person', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('1.0'))])),
                ('collect_payments', models.BooleanField(default=False)),
                ('players_can_change_team', models.BooleanField(default=False)),
                ('organiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
