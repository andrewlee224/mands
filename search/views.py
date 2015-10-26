import urllib2
import json

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from mands import api_settings

# Create your views here.

def search(request):
    context = RequestContext(request)
    context_dict = {}

    search_term = request.GET.get('search_term', '')

    if search_term:
        settings_dict = api_settings.APIS['api-dev']
        url_opener = urllib2.build_opener()
        url_opener.addheaders = [
            ('Authorization', settings_dict['headers']['Authorization'])
        ]

        try:
            api_response = url_opener.open(
                settings_dict['search_url'] + "?searchTerm=" + search_term)

            api_response = json.load(api_response)

            context_dict['items'] = api_response['search']['results']
        except (urllib2.HTTPError, ValueError, KeyError):
            error_found = True
        else:
            error_found = False
        context_dict['error'] = error_found

    context_dict['search_term'] = search_term

    return render_to_response('search/search.html', context_dict, context)
