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

        # validate url
        url = params.get('url')
        validate = URLValidator()

        try:
            validate(url)
        except:
            res = HttpResponse()
            res.status_code = 400
            res.content = "Not a valid URL"
            return res

        # generate shortid and make new url in db
        shorty = sid.generate()
        host = request.get_host()
        secure = request.is_secure()
        short_url = ""
        if secure:
            short_url = f"https://{host}/{shorty}"
        else:
            short_url = f"http://{host}/{shorty}"

        link = Link(long=url, short=short_url)
        link.save()

        return JsonResponse({'shorturl': link.short})

    return HttpResponse(status=400, content="Bad request body or wrong request type (POST only)")


def get_link(request, url):
    # Link.get
    return HttpResponse(url)


def generate_short_url(long_url):
    pass
