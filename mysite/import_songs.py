from songs.models import Song, Artist

path = r"/Users/daniel/emelody/mysite/songs.txt"
f = open(path, 'r')
songs = []
for line in f:
    # Lines are in the following format:
    # Artist - Title.mp3
    line = line.replace('.mp3', '')
    line = line.split(' - ')
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
    artist = song[0]
    title = song[1]
    try:
        db_song = Song.objects.get(title=title, artist=artist)
    except Song.DoesNotExist:
        db_song = Song(title=title, artist=artist)
        db_song.save()

