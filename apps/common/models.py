from django.db import models

# Create your models here.


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=255)
    site_logo = models.FileField(upload_to='site/logo/', blank=True, null=True)
    site_favicon = models.FileField(upload_to='site/favicon/', blank=True, null=True)
    site_logo_footer = models.FileField(upload_to='site/logo_footer/', blank=True, null=True)
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField()
    meta_image = models.FileField(upload_to='site/meta/', blank=True, null=True)
    smpt = models.CharField(max_length=200, blank=True, null=True)
    smtp_pass = models.CharField(max_length=200, blank=True, null=True)
    telegram_bot = models.CharField(max_length=255, blank=True, null=True)

