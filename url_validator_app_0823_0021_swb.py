# 代码生成时间: 2025-08-23 00:21:49
from django.conf.urls import url
from django.http import HttpResponse
from django.views import View
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
import re

"""
URL Validator App

This application provides functionality to validate the
validity of a given URL.
"""

class URLValidator:
    def __init__(self):
        self.url_pattern = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https:// or ftp:// or ftps://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
            r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|' # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
            r'(?::[0-9]+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def is_valid_url(self, url):
        """
        Validate the URL.

        Args:
            url (str): The URL to validate.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        return bool(self.url_pattern.match(url))


class URLValidationView(View):
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to validate URL.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: A response with the validation result.
        """
        url_to_validate = request.GET.get('url')
        if not url_to_validate:
            return HttpResponse("Please provide a URL to validate.", status=400)

        try:
            url_validator = URLValidator()
            if url_validator.is_valid_url(url_to_validate):
                return HttpResponse(f"The URL {url_to_validate} is valid.", status=200)
            else:
                return HttpResponse(f"The URL {url_to_validate} is not valid.", status=400)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)

# Define URL patterns for the URL validator view.
urlpatterns = [
    url(r'^validate-url/$', URLValidationView.as_view(), name='validate-url'),
]
