from django.shortcuts import render_to_response
from django.http import HttpResponse
from songs.models import Song

# Create your views here.

def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        else:
            songs = Song.objects.filter(title__icontains=q)
            return render_to_response('search_results.html', {'songs': songs, 'query': q})
    return render_to_response('search_form.html', {'errors': errors})