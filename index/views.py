import json
from django.http import HttpResponse
from .autocheck import CheckIn


def index(request):
    autocheck = CheckIn()
    res = autocheck.user_check_in()
    print(json.loads(res))
    return HttpResponse(res)
