from rest_framework import serializers


class UrlSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=1000)
    date = serializers.DateTimeField()
    short_url = serializers.CharField(max_length=20)


class PostRequestsToUrlSerializer(serializers.Serializer):
    ip_address = serializers.CharField(max_length=100)
    user_agent = serializers.CharField(max_length=1000)
    referer = serializers.CharField(max_length=1000)
    date = serializers.DateTimeField()
    url_id = serializers.IntegerField()


class CountRequestsToShortUrlSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    date = serializers.DateTimeField()
    url_id = serializers.IntegerField()