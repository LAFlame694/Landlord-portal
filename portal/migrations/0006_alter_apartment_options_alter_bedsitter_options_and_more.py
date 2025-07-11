# Generated by Django 5.2.1 on 2025-06-21 21:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_receipt_tenant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apartment',
            options={'verbose_name_plural': 'Apartments'},
        ),
        migrations.AlterModelOptions(
            name='bedsitter',
            options={'verbose_name_plural': 'Bedsitters'},
        ),
        migrations.AlterModelOptions(
            name='invoice',
            options={'verbose_name_plural': 'Invoices'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name_plural': 'Payments'},
        ),
        migrations.AlterModelOptions(
            name='receipt',
            options={'verbose_name_plural': 'Receipts'},
        ),
        migrations.AlterModelOptions(
            name='tenantprofile',
            options={'verbose_name': 'Tenant Profile', 'verbose_name_plural': 'Tenant Profiles'},
        ),
        migrations.AddField(
            model_name='invoice',
            name='apartment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='portal.apartment'),
            preserve_default=False,
        ),
    ]
