from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound, JsonResponse)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import (require_GET, require_http_methods,
                                          require_POST)


def login_required_here(f):
    """ Documentation for login_required_here """

    def function_with_login(request):
        username, password = request.POST.get('user'), request.POST.get('pass')
        if not username or not password:
            return HttpResponseBadRequest('user or pass not found')
        try:
            u = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            return HttpResponseNotFound('User not found!')
        return f(request)

    return function_with_login


@require_POST
@csrf_exempt
def signup(request):
    username, password = request.POST.get('user'), request.POST.get('pass')
    if not username or not password:
        return HttpResponseBadRequest('user or pass not found')
    if User.objects.filter(username=username).exists():
        return HttpResponse('Duplicate username.')
    else:
        User.objects.create_user(username=username, password=password)
        return HttpResponse('User created')


@require_POST
@csrf_exempt
def signin(request):
    username, password = request.POST.get('user'), request.POST.get('pass')
    if not username or not password:
        return HttpResponseBadRequest('user or pass not found')
    if authenticate(username=username, password=password):
        return HttpResponse('Authenticated')
    else:
        return HttpResponseNotFound('Bad credentials')
