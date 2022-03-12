from django.db import models


class Url(models.Model):
    url = models.CharField(max_length=1000)
    date = models.DateTimeField()
    short_url = models.CharField(max_length=20)


class PostRequestsToUrl(models.Model):
    ip_address = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=1000)
    referer = models.CharField(max_length=1000)
    date = models.DateTimeField()
    url_id = models.ForeignKey(Url, on_delete=models.CASCADE)


class CountRequestsToShortUrl(models.Model):
    count = models.IntegerField()
    date = models.DateTimeField()
    url_id = models.ForeignKey(Url, on_delete=models.CASCADE)


