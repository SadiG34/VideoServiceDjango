# Generated by Django 5.0.4 on 2024-04-23 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videoservice', '0008_subscription_delete_subscribers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]