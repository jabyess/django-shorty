from django.shortcuts import redirect
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ObjectDoesNotExist
from .utils import build_short_url, build_day_count
from .models import Link, Visit
from shortid import ShortId
import json

sid = ShortId()

def noop(wat):
    return HttpResponse("Nothing to see here. Try reading the docs")

@csrf_exempt
def make_link(request):
    if request.method == "POST" and len(request.body) > 0:

        params = json.loads(request.body)

        # key validation
        keys = params.keys()

        if len(keys) > 1 or 'url' not in keys:
            res = HttpResponse()
            res.status_code = 400
            res.content = 'Please provide a json object with the format { "url" : "http://example.com" }'
            return res

        # url validation
        url = params.get('url')
        validate = URLValidator()

        try:
            validate(url)
        except:
            res = HttpResponse()
            res.status_code = 400
            res.content = "Not a valid URL"
            return res

        # look up link by long url
        try:
            Link.objects.get(long=url)
        except ObjectDoesNotExist:
            # if doesnotexist:
            # generate shortid and make new url in db
            # add 1 visit record
            shorty = sid.generate()
            short_url = build_short_url(
                request.is_secure(), request.get_host(), shorty)

            link = Link(long=url, short=short_url)
            link.save()
            visit = Visit(link_id=link.id)
            visit.save()

            # return newly created short link
            return JsonResponse({"shorturl": link.short})

        # if link exists already, return it
        found = Link.objects.get(long=url)
        return JsonResponse({'shorturl': found.short})

    return HttpResponse(status=400, content="Bad request body or wrong request type (POST only)")


def get_link(request, shortid):
    if request.method == "GET":
        # build url so that db lookup works
        short_url = build_short_url(
            request.is_secure(), request.get_host(), shortid)

        # look up by short url and return redirect to long url
        # add visit 
        try:
            link = Link.objects.get(short=short_url)
            v = Visit(link_id=link.pk)
            v.save()
        except:
            return HttpResponse(status=404, content="No url found")

        return redirect(link.long)

    return HttpResponse(status=400)


def get_stats(request, shortid):
    # build url so that db lookup works
    full_short = build_short_url(request.is_secure(), request.get_host(), shortid)
    link = Link.objects.get(short=full_short)
    # get all visit records by link id
    visits = Visit.objects.filter(link_id=link.id)

    # build stats object 
    results = {
        "total_visits": len(visits),
        "created": link.created,
        "visits_per_day" : build_day_count(visits)
    }

    return JsonResponse(results)