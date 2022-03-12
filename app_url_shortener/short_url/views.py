from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Url
from .models import CountRequestsToShortUrl
from .models import PostRequestsToUrl
from .serializers import UrlSerializer
import re
import hashlib
import datetime
from django.shortcuts import redirect


class UrlView(APIView):
    def get(self, request):
        urls = Url.objects.all()
        serializer = UrlSerializer(urls, many=True)
        return Response({"urls": serializer.data}, status=200)

    def post(self, request):
        url = request.data.get('url')
        if self.check_link_validity(url):
            data = Url.objects.filter(url=url)
            if data:
                short_url = data[0].short_url
                url_id = data[0]
                self.add_to_post_requests_to_url(request, url_id)
                return Response({"shortened_url": short_url}, status=200)
            hash_url = self.hash_link(url)
            date = datetime.datetime.now()
            new_url = Url.objects.create(url=url, date=date, short_url=hash_url)
            new_url.save()
            self.add_to_post_requests_to_url(request, new_url)
            return Response({"shortened_url": hash_url}, status=201)
        return Response({"error": "url invalid"}, status=400)

    def add_to_post_requests_to_url(self, request, url_id):
        user_agent = request.headers.get('User-Agent')
        referer = request.headers.get('referer')
        ip_address = self.get_client_ip(request)
        date = datetime.datetime.now()
        PostRequestsToUrl.objects.create(ip_address=ip_address, user_agent=user_agent, referer=referer, date=date, url_id=url_id).save()

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def check_link_validity(self, url):
        if re.match('http', url) is None:
            return False
        return True

    def hash_link(self, link: str):
        res = hashlib.md5(link.encode('utf-8')).hexdigest()
        return res[:7]  # return first seven symbols


class ShortenedUrlsCountView(APIView):
    def get(self, request):
        count = Url.objects.all().count()
        data = {"count": count}
        return Response(data=data, status=200)


class TenMostPopularUrlView(APIView):
    def get(self, request):
        data = CountRequestsToShortUrl.objects.select_related('url_id').order_by('-count')[:10]
        #print(data.query)
        to_return = []
        for el in data:
            to_return.append({"count": el.count, "url": el.url_id.url, "short_url": el.url_id.short_url})
        return Response(to_return, status=200)


class ShortenUrlView(APIView):
    def get(self, request, shortened_url):
        url_query_set = Url.objects.filter(short_url=shortened_url)
        if url_query_set:
            url_for_redirect = url_query_set[0].url

            count_requests_query_set = CountRequestsToShortUrl.objects.filter(url_id=url_query_set[0])
            if count_requests_query_set:
                count_requests_query_set[0].count += 1
                count_requests_query_set[0].save()
            else:
                date = datetime.datetime.now()
                CountRequestsToShortUrl.objects.create(count=1, date=date, url_id=url_query_set[0])

            return redirect(url_for_redirect, status=302)
        return Response({"url not found, go away"}, status=404)