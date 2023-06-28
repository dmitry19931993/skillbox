from django.http import HttpRequest
from django.shortcuts import render
import time


def set_useragent_request_middleware(get_response):

    print('initial call')

    def middleware(request: HttpRequest):
        print('before_get_response')
        request.user_agent = request.META['HTTP_USER_AGENT'] + "asa" + request.META.get("REMOTE_ADDR", None)
        response = get_response(request)
        print('after_get_response')
        return response

    return middleware

class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0
        self.url_dict = {}

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print('requests count: ', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('responses count : ', self.responses_count)
        response = self.throttling_middleware(request)
        return response

    def process_exception(self, request: HttpRequest, exeption: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exceptions so far')

    def throttling_middleware(self, request: HttpRequest):
        user_url = request.META.get("REMOTE_ADDR", None)
        time_now = time.time()
        if user_url in self.url_dict:
            time_different = time_now - self.url_dict[user_url]
            if time_different < 5:
                self.url_dict[user_url] = time.time()
                return render(request, "requestdataapp/error_url.html")
        self.url_dict[user_url] = time.time()
        print(self.url_dict)
        response = self.get_response(request)
        return response