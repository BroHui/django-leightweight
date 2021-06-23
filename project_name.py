# coding: utf-8
import sys
import os
from functools import wraps

from django.conf import settings
from django.urls import path
from django.http import HttpResponse, HttpResponseForbidden
from django.core.wsgi import get_wsgi_application

DEBUG = os.getenv('DEBUG', '0') == '1'
SECRET_KEY = os.getenv('SECRET_KEY', '{{ secret_key }}')
ALLOW_HOST = os.getenv('ALLOW_HOST', 'localhost').split(',')
TOKEN_LIST = os.getenv('TOKEN_LIST', '')
TOKEN_LIST = TOKEN_LIST.split(',') if TOKEN_LIST else []
if not TOKEN_LIST: print("Run server as NO AUTH mode!")
settings.configure(
    DEBUG=DEBUG,
    ROOT_URLCONF=__name__,
    SECRET_KEY=SECRET_KEY,
    ALLOW_HOST=ALLOW_HOST,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
    ),
    TOKEN_LIST=TOKEN_LIST
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