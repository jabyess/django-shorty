from django.shortcuts import redirect
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from .utils import build_short_url
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
        short_url = build_short_url(request.is_secure(), request.get_host(), shorty)

        link = Link(long=url, short=short_url)
        print(link.stats)
        link.save()

        return JsonResponse({'shorturl': link.short})

    return HttpResponse(status=400, content="Bad request body or wrong request type (POST only)")


def get_link(request, shortid):
    if request.method == "GET":
        short_url = build_short_url(request.is_secure(), request.get_host(), shortid)

        # look up long url and return redirect
        try:
            link = Link.objects.get(short=short_url)
        except:
            return HttpResponse(status=404, content="No url with that structure")

        return redirect(link.long)

    return HttpResponse(status=400)


