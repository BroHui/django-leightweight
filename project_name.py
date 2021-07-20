# coding: utf-8
import sys
import os
import json
from functools import wraps

from django.conf import settings
from django.urls import path
from django.http import HttpResponse, HttpResponseForbidden
from django.core.wsgi import get_wsgi_application
from django.db import connection

from rq import Queue
from redis import Redis
redis_conn = Redis(host='redis')
q = Queue(connection=redis_conn)

DEBUG = os.getenv('DEBUG', '0') == '1'
SECRET_KEY = os.getenv('SECRET_KEY', '{{ secret_key }}')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
TOKEN_LIST = os.getenv('TOKEN_LIST', '')
TOKEN_LIST = TOKEN_LIST.split(',') if TOKEN_LIST else []
if not TOKEN_LIST: print("Run server as NO AUTH mode!")
settings.configure(
    DEBUG=DEBUG,
    ROOT_URLCONF=__name__,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
    ),
    TOKEN_LIST=TOKEN_LIST,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }
)
"""  Simple auth  """


def verify_request(func):
    @wraps(func)
    def returned_wrapper(request, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        request_ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        # Auth
        token = request.GET.get('token', '')
        if settings.TOKEN_LIST and (not token or token not in settings.TOKEN_LIST):
            print(f'Unauthorized Request from {request_ip}')
            return HttpResponseForbidden()
        # get dict
        get_dict = request.GET.dict()
        request.param = lambda x: get_dict.get(x, '')
        # get body
        request_body = request.body
        if request_body:
            try:
                request.json = json.loads(request_body)
            except json.decoder.JSONDecodeError:
                print('+verify_request Error: parse request body to json failed')
                request.json = {}
        return func(request, *args, **kwargs)

    return returned_wrapper


"""  Your Views here """


@verify_request
def index(request):
    return HttpResponse('Django works!')


urlpatterns = [
    path('', index),
]
# uWSGI Supports
application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
