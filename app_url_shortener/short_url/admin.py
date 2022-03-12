from django.contrib import admin

# Register your models here.
from .models import Url, PostRequestsToUrl, CountRequestsToShortUrl
admin.site.register(Url)
admin.site.register(PostRequestsToUrl)
admin.site.register(CountRequestsToShortUrl)