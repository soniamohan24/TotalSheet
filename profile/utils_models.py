from django.db import models


class Website(models.Model):
    url = models.URLField(blank=True, null=True)


class Socials(models.Model):
    TYPE = (
        ("fb", "Facebook"),
        ("insta", "Instagram"),
        ("whatsapp", "WhatsApp"),
        ("x", "X"),
        ("linkedin", "LinkedIn"),
        ("youtube", "YouTube"),
        ("tiktok", "TikTok"),
        ("snapchat", "Snapchat"),
        ("telegram", "Telegram"),
        ("other", "Other"),
    )
    social_type = models.CharField(choices=TYPE, blank=True, null=True)
    link = models.CharField(blank=True, null=True)
