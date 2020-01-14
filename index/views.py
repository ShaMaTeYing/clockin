import json
from django.http import HttpResponse
from .autocheck import CheckIn


def index(request):
    autocheck = CheckIn()
    res = autocheck.user_check_in()
    print(json.loads(res.decode('utf-8')))
    return HttpResponse(res)
