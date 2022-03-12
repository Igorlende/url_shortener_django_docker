from django.urls import path
from .views import UrlView
from .views import ShortenedUrlsCountView
from .views import TenMostPopularUrlView
from .views import ShortenUrlView

app_name = "short_url"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('shortened_url/', UrlView.as_view()),
    path('shortened_urls_count/', ShortenedUrlsCountView.as_view()),
    path('ten_most_popular_url/', TenMostPopularUrlView.as_view()),
    path('<str:shortened_url>/', ShortenUrlView.as_view()),

]
