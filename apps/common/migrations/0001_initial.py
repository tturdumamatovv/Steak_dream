# Generated by Django 5.1.1 on 2024-09-19 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=255)),
                ('site_logo', models.FileField(blank=True, null=True, upload_to='site/logo/')),
                ('meta_title', models.CharField(max_length=255)),
                ('meta_description', models.TextField()),
                ('meta_image', models.FileField(blank=True, null=True, upload_to='site/meta/')),
                ('smpt', models.CharField(blank=True, max_length=200, null=True)),
                ('smtp_pass', models.CharField(blank=True, max_length=200, null=True)),
                ('telegram_bot', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
