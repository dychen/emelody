import datetime
import random
import json
import urllib

from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from mysite.forms import ContactForm

from songs.models import Song, Artist, Rating

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.db.models.loading import get_model

def homepage(request):
    is_logged_in = request.user.is_authenticated()
    if is_logged_in:
        username = request.user.username
    else:
        username = None
    current_date = datetime.datetime.now()
    return render_to_response('homepage.html', 
                              {'is_logged_in': is_logged_in, 
                              'username': username, 
                              'current_date': current_date})

#
# User Login/Registration Views
#

# Used the default python login/logout views:
# login
# logout

@csrf_exempt
def register(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect('/accounts/register/success')
    else:
        form = UserCreationForm()
    return render_to_response('registration/register.html', {'form': form})

def registration_successful(request):
    return render_to_response('registration/success.html')

#
# User Profile/Rating Views
#

@csrf_exempt
def profile(request):
    is_logged_in = request.user.is_authenticated()
    if is_logged_in:
        username = request.user.username
    else:
        username = None

    songs = Song.objects.all()
    ratings = Rating.objects.filter(username=request.user)
    num_ratings = len(ratings)
    
    # Code that handles search filtering
    # Song search
    errors = []
    if 'q_songs' in request.GET or 'q_artists' in request.GET:
        if 'q_songs' in request.GET:
            q = request.GET['q_songs']
        elif 'q_artists' in request.GET:
            q = request.GET['q_artists']
        else:
            raise Exception('Error: Unhandled GET request.')
        if not q:
            errors.append('Enter a search term.')
        # If there were errors in the search query, return them.
        if len(errors) != 0:
            return render_to_response('userpages/profile.html',
                                      {'is_logged_in': is_logged_in,
                                      'username': username,
                                      'songs': songs,
                                      'ratings': ratings,
                                      'errors': errors})
        # Otherwise, execute the search query.
        else:
            queried = True
            if 'q_songs' in request.GET:
                songs = Song.objects.filter(title__icontains=q)
            elif 'q_artists' in request.GET:
                songs = Song.objects.filter(artist__name__icontains=q)
            else:
                raise Exception('Error: Unhandled GET request.')
            return render_to_response('userpages/profile.html',
                                      {'is_logged_in': is_logged_in,
                                      'username': username,
                                      'songs': songs,
                                      'ratings': ratings,
                                      'query': q,
                                      'queried': queried})

    # Code that handles the random song button
    if 'random_song' in request.GET:
        try:
            song = random_song_all()
        except ValueError:
            return Http404()
        return HttpResponseRedirect('/rate/'+str(song.id))
                
    # TODO: Code that handles the recommend song button
    if 'recommend_song' in request.GET:
        # TODO: Recommender logic here...
        # For now, just give a random song...
        try:
            song = random_song_all()
        except ValueError:
            return Http404()
        return HttpResponseRedirect('/rate/'+str(song.id))

    # Code that handles the filter unrated songs button
    if 'show_unrated' in request.GET:
        unrated = True;
        songs = Song.objects.exclude(rating__username__exact=request.user)
        return render_to_response('userpages/profile.html', 
                                  {'is_logged_in': is_logged_in, 
                                  'username': username,
                                  'songs': songs,
                                  'ratings': ratings,
                                  'unrated': unrated})

    # If there is wasn't search query, just return the normal form.
    return render_to_response('userpages/profile.html', 
                              {'is_logged_in': is_logged_in, 
                              'username': username,
                              'songs': songs,
                              'ratings': ratings})

@csrf_exempt
def rate(request, song_id):
    is_logged_in = request.user.is_authenticated()
    if is_logged_in:
        username = request.user.username
    else:
        username = None
    
    try:
        song = Song.objects.get(id=song_id)
    except ValueError:
        return Http404()
    ratings = Rating.objects.filter(username=request.user)
    
    rating = 0
    if 'rate_1' in request.POST:
        rating = 1
    elif 'rate_2' in request.POST:
        rating = 2
    elif 'rate_3' in request.POST:
        rating = 3
    elif 'rate_4' in request.POST:
        rating = 4
    elif 'rate_5' in request.POST:
        rating = 5

    if rating != 0:
        # Check to see if the user has already rated the song.
        try: 
            r = Rating.objects.get(username=request.user, song=song)
        # If he hasn't, make a new rating tuple.
        except Rating.DoesNotExist:
            r = Rating(username=request.user, 
                       song=song, 
                       rating=rating)
        # If he has, update the existing rating.
        else:
            r.rating = rating
        r.save()
        return HttpResponseRedirect('success/')

    else:
        # Loads another random song for "rate next."
        songs = Song.objects.exclude(rating__username__exact=request.user)
        try:
            next_song = random_song(songs)
        except ValueError:
            return Http404()
        
        youtube_link = get_embedded_link(get_video(song.title, song.artist.name))
        return render_to_response('userpages/rate.html', 
                                  {'is_logged_in': is_logged_in, 
                                  'username': username, 
                                  'song': song,
                                  'ratings': ratings,
                                  'youtube_link': youtube_link,
                                  'next_song': next_song})

def rate_successful(request):
    is_logged_in = request.user.is_authenticated()
    if is_logged_in:
        username = request.user.username
    else:
        username = None
    
    songs = Song.objects.exclude(rating__username__exact=request.user)
    try:
        song = random_song(songs)
    except ValueError:
        return Http404()

    return render_to_response('userpages/rate_successful.html', 
                              {'is_logged_in': is_logged_in, 
                              'username': username,
                              'song': song})

#
# Helper Functions
#

# Returns a random song from the database.
def random_song_all():
    songs = Song.objects.all()
    return random_song(songs)

# Returns a random song from a list of songs.
def random_song(songs):
    rand_index = random.randint(0, len(songs) - 1)
    return songs[rand_index]

# Takes in a title string and artist string, finds the first Youtube result, and
# returns the link as a string.
def get_video(title, artists): 
    query = title
    for i in artists:
        query += '+' + i
    query += '+-Cover'
    url = 'http://gdata.youtube.com/feeds/api/videos?q=' + query + '&max-results=1&alt=json'
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data['feed']['entry'][0]['link'][0]['href']

# Takes in a Youtube url and returns the embedded url as a string.
def get_embedded_link(url):
    start_index = url.find('watch?v=') + 8
    stop_index = url.find('&feature')
    video_id = url[start_index:stop_index]
    embedded_url = 'http://www.youtube.com/embed/' + video_id
    return embedded_url
    
#
# Administration Functions
#

def update_db(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        upload_songs()
        return render_to_response('admin/db_update_successful.html')
    else:
        return render_to_response('permission_denied.html')
        

# Uploads all songs to the database
def upload_songs():
    path = r"/Users/daniel/emelody/mysite/songs.txt"
    f = open(path, 'r')
    songs = []
    for line in f:
        # Lines are in the following format:
        # Artist - Title.mp3
        line = line.replace('.mp3', '')
        line = line.split('-')
        artist = line[0].strip()
        song = line[1].strip()
        songs.append((artist, song))

    f.close()

    # Populate the Artist table
    for song in songs:
        artist = song[0]
        try: 
            db_artist = Artist.objects.get(name=artist)
        except Artist.DoesNotExist:
            db_artist = Artist(name=artist)
            db_artist.save()

    # Populate the Song table
    for song in songs:
        artist_name = song[0]
        title = song[1]
        try:
            artist = Artist.objects.get(name=artist_name)
            try:
                db_song = Song.objects.get(title=title, artist=artist)
            except Song.DoesNotExist:
                db_song = Song(title=title, artist=artist)
                db_song.save()
        except Artist.DoesNotExist:
            continue
