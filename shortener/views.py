from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from .models import Link, Stats
from shortid import ShortId 
import json

sid = ShortId()
# Create your views here.

def noop(wat):
    return HttpResponse("wat")

@csrf_exempt
def make_link(request):
    if request.method == "POST" and len(request.body) > 0:

        params = json.loads(request.body)

        # quick validation
        keys = params.keys()

        if len(keys) > 1 or 'url' not in keys:
            res = HttpResponse()
            res.status_code = 400
            res.content = 'Please provide a json object with the format { "url" : "http://example.com" }' 
            return res
        
        # make new url in db
        url = params.get('url')

        shorty = sid.generate()
        host = request.get_host()
        short_url = f"http://{host}/{shorty}"

        validate = URLValidator()
        
        try:
            validate(url)
        except:
            res = HttpResponse()
            res.status_code = 400
            res.content = "Not a valid URL"
            return res

        link = Link(long=url, short=short_url)
        link.save()

        return JsonResponse({ 'shorturl': link.short })
    return JsonResponse({ "test" : False })
        

def get_link(request, url):
    return HttpResponse(url)


def generate_short_url(long_url):
    pass