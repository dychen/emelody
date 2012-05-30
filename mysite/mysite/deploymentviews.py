import datetime
import random
import json
import urllib

from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from mysite.forms import ContactForm, CustomUserCreationForm

from songs.models import Song, Artist, Rating, RecommendedSong, RecommendedArtist, SimilarUser, SimilarSong, Playlist, Location
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

from django.db.models.loading import get_model

from performances import *

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

def get_started(request):
    is_logged_in = request.user.is_authenticated()
    if is_logged_in:
        username = request.user.username
    else:
        username = None
    return render_to_response('get_started.html', 
                              {'is_logged_in': is_logged_in, 
                              'username': username})

def about(request):
    is_logged_in = request.user.is_authenticated()
    if is_logged_in:
        username = request.user.username
    else:
        username = None
    return render_to_response('about.html', 
                              {'is_logged_in': is_logged_in, 
                              'username': username})

def contact(request):
    is_logged_in = request.user.is_authenticated()
    if is_logged_in:
        username = request.user.username
    else:
        username = None
    return render_to_response('contact.html', 
                              {'is_logged_in': is_logged_in, 
                              'username': username})

#
# User Login/Registration Views
#

# Used the default python login/logout views:
# login
# logout

def logout_view(request):
    calculate_ratings()
    
    # export_ratings()
    # Repopulate the RecommendedSong, SimilarUser, and SimilarSong tables.
    # import_recommended_songs()
    # import_similar_users()
    # import_similar_songs()
    # Repopulate the RecommendedArtist table.
    # calculate_recommended_artists()
    
    calculate_concerts()
    
    logout(request)
    return render_to_response('registration/logged_out.html')
    # Redirect to a success page.

@csrf_exempt
def register(request):
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            new_user = form.save()
            user_location = Location(username=new_user, state=state)
            user_location.save()
            return HttpResponseRedirect('/accounts/register/success')
    else:
        form = CustomUserCreationForm()
    return render_to_response('registration/register.html', {'form': form})

def registration_successful(request):
    return render_to_response('registration/success.html')

# Old registration code
'''@csrf_exempt
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
    return render_to_response('registration/success.html')'''





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
    
    playlists = Playlist.objects.filter(username=request.user)
    songs = Song.objects.all()

    # Code that handles displaying similar users
    similar_users = SimilarUser.objects.filter(username=request.user).order_by('score')[:5]
    similar_songs = {}
    for similar_user in similar_users:
        similar_songs[similar_user] = RecommendedSong.objects.filter(username=similar_user.username).order_by('-predicted_rating')[:5]
    
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
                                      'playlists': playlists,
                                      'errors': errors,
                                      'similar_songs': similar_songs})
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
                                      'playlists': playlists,
                                      'query': q,
                                      'queried': queried,
                                      'similar_songs': similar_songs})
    

    # If there is wasn't search query, just return the normal form.
    return render_to_response('userpages/profile.html', 
                              {'is_logged_in': is_logged_in, 
                              'username': username,
                              'songs': songs,
                              'playlists': playlists,
                              'similar_songs': similar_songs})

@csrf_exempt
def create_playlist(request, song_id):
    is_logged_in = request.user.is_authenticated()
    if is_logged_in:
        username = request.user.username
    else:
        username = None
    
    try:
        song = Song.objects.get(id=song_id)
    except ValueError:
        return Http404()
    
    errors = []
    if 'title' in request.GET:
        q = request.GET['title']
        if not q:
            errors.append('Enter a title for your playlist.')
        try:
            db_playlist = Playlist.objects.get(username=request.user, song=song)
            errors.append('You already have a playlist based on this song. Please go back and choose another song.')
        except Playlist.DoesNotExist:
            # Do nothing.
            pass
            
        # If there were errors in the form, return them.
        if len(errors) != 0:
            return render_to_response('userpages/create_playlist.html',
                                      {'is_logged_in': is_logged_in,
                                      'username': username,
                                      'song': song,
                                      'errors': errors})
        # Otherwise, create the playlist.
        else:
            db_playlist = Playlist(username=request.user, title=q, song=song)
            db_playlist.save()
            return HttpResponseRedirect('success/')

    else:
        return render_to_response('userpages/create_playlist.html',
                                  {'is_logged_in': is_logged_in,
                                  'username': username,
                                  'song': song})

def create_playlist_successful(request):
    is_logged_in = request.user.is_authenticated()
    if is_logged_in:
        username = request.user.username
    else:
        username = None
    
    return render_to_response('userpages/create_playlist_successful.html', 
                              {'is_logged_in': is_logged_in, 
                              'username': username})

@csrf_exempt
def listen(request, playlist_id):
    is_logged_in = request.user.is_authenticated()
    if is_logged_in:
        username = request.user.username
    else:
        username = None
    
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        if request.user != playlist.username:
            return render_to_response('permission_denied.html')
    except ValueError:
        return Http404()

    ratings = Rating.objects.filter(username=request.user)
    song = playlist.song
    playlist_songs = SimilarSong.objects.filter(song=song).order_by('score')[:100]
    playlist_song = random_song(playlist_songs).similar_song

    youtube_link = get_embedded_link(get_video(playlist_song.title, playlist_song.artist.name))
    
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
            r = Rating.objects.get(username=request.user, song=playlist_song)
        # If he hasn't, make a new rating tuple.
        except Rating.DoesNotExist:
            r = Rating(username=request.user, 
                       song=playlist_song, 
                       rating=rating)
        # If he has, update the existing rating.
        else:
            r.rating = rating
        r.save()
        rated = True
        return render_to_response('userpages/listen.html', 
                                  {'is_logged_in': is_logged_in, 
                                  'username': username, 
                                  'song': playlist_song,
                                  'ratings': ratings,
                                  'youtube_link': youtube_link,
                                  'rated': rated,
                                  'playlist_id': playlist_id})

    else:        
        return render_to_response('userpages/listen.html', 
                                  {'is_logged_in': is_logged_in, 
                                  'username': username, 
                                  'song': playlist_song,
                                  'ratings': ratings,
                                  'youtube_link': youtube_link,
                                  'playlist_id': playlist_id})

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

# UNUSED
# Exports the rating table to a text file.
'''
def export_ratings():
    ratings = Rating.objects.all()
    path = r"/Users/daniel/emelody/mysite/learning/ratings.txt"
    
    f = open(path, 'w')
    for rating in ratings:
        user = str(rating.username_id)
        song = str(rating.song_id)
        rating = str(rating.rating)
        f.write(user + ' ' + song + ' ' + rating + '\n')
    f.close()
'''

# Imports data from a text file to the recommendedsong table.
def import_recommended_songs():
    path = r"/Users/daniel/emelody/mysite/learning/predicted_ratings.txt"
    
    f = open(path, 'r')
    recommended_songs = []
    for line in f:
        # Lines are in the following format:
        # username_id song_id projected_rating
        line = line.split(' ')
        username_id = line[0]
        song_id = line[1]
        projected_rating = line[2]
        recommended_songs.append((username_id, song_id, projected_rating))
    f.close()
    
    # Populate the RecommendedSong table
    for recommended_song in recommended_songs:
        username_id = recommended_song[0]
        song_id = recommended_song[1]
        predicted_rating = recommended_song[2]
        try: 
            username = User.objects.get(id=username_id)
            song = Song.objects.get(id=song_id)
            try:
                db_recommended_song = RecommendedSong.objects.get(username=username, song=song)
                db_recommended_song.predicted_rating = predicted_rating
                db_recommended_song.save()
            except RecommendedSong.DoesNotExist:
                db_recommended_song = RecommendedSong(username=username, 
                                                      song=song, 
                                                      predicted_rating=predicted_rating)
                db_recommended_song.save()
        except User.DoesNotExist:
            # This shouldn't happen.
            return Http404()
        except Song.DoesNotExist:
            # This shouldn't happen.
            return Http404()

# Imports data from a text file to the similaruser table.
def import_similar_users():
    path = r"/Users/daniel/emelody/mysite/learning/u_similarity.txt"
    
    # Read in the file
    f = open(path, 'r')
    similar_users = []
    for line in f:
        # Lines are in the following format:
        # song_id other_song_id score
        line = line.split(' ')
        username_id = line[0]
        other_username_id = line[1]
        score = line[2]
        similar_users.append((username_id, other_username_id, score))
    f.close()
    
    # Populate the SimilarUser table
    for similar_user in similar_users:
        username_id = similar_user[0]
        other_username_id = similar_user[1]
        score = similar_user[2]
        try:
            username = User.objects.get(id=username_id)
            other_username = User.objects.get(id=other_username_id)
            try:
                db_similar_user = SimilarUser.objects.get(username=username, similar_user=other_username)
                db_similar_user.score = score
                db_similar_user.save()
            except SimilarUser.DoesNotExist:
                db_similar_user = SimilarUser(username=username, 
                                              similar_user=other_username, 
                                              score=score)
                db_similar_user.save()
        except User.DoesNotExist:
            # This shouldn't happen.
            return Http404()

# Imports data from a text file to the similarsong table.
def import_similar_songs():
    path = r"/Users/daniel/emelody/mysite/learning/m_similarity.txt"
    
    # Read in the file
    f = open(path, 'r')
    similar_songs = []
    for line in f:
        # Lines are in the following format:
        # song_id other_song_id score
        line = line.split(' ')
        song_id = line[0]
        other_song_id = line[1]
        score = line[2]
        similar_songs.append((song_id, other_song_id, score))
    f.close()
    
    # Populate the SimilarSong table
    for similar_song in similar_songs:
        song_id = similar_song[0]
        other_song_id = similar_song[1]
        score = similar_song[2]
        try: 
            song = Song.objects.get(id=song_id)
            other_song = Song.objects.get(id=other_song_id)
            try:
                db_similar_song = SimilarSong.objects.get(song=song, similar_song=other_song)
                db_similar_song.score = score
                db_similar_song.save()
            except SimilarSong.DoesNotExist:
                db_similar_song = SimilarSong(song=song, 
                                              similar_song=other_song, 
                                              score=score)
                db_similar_song.save()
        except Song.DoesNotExist:
            # This shouldn't happen.
            return Http404()

# Populates the RecommendedArtist table from the RecommendedSong table.
def calculate_recommended_artists():
    # Clear the RecommendedArtist table
    RecommendedArtist.objects.all().delete()
    
    users = User.objects.all()
    for user in users:
        top_songs = Song.objects.filter(recommendedsong__username=user, recommendedsong__predicted_rating__gt=3.0)
        for song in top_songs:
            artist = song.artist
            try:
                db_recommended_artist = RecommendedArtist.objects.get(username=user, artist=artist)
                db_recommended_artist.count += 1
                db_recommended_artist.save()
            except RecommendedArtist.DoesNotExist:
                db_recommended_artist = RecommendedArtist(username=user, artist=artist, count=1)
                db_recommended_artist.save()
            


# Runs transform.py, which calculates predicted ratings of all users.
def calculate_ratings():
    path = r"/Users/daniel/emelody/mysite/learning/transform.py"
    execfile(path)
    
# Populates the concert table.
def calculate_concerts():
    for user in User.objects.all():
        artists = list(Artist.objects.filter(recommendedartist__username=user))
        location = Location.objects.get(username=user)
        concerts = getconcerts(artists, location)
        for concert in concerts:
            artist = concert[0]
            date = concert[1]
            venue = concert[2]
            location = concert[3]
            url = concert[4]
            new_concert = Concert(username=user, artist=artist, date=date, venue=venue, location=location, url=url)
            new_concert.save()


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


