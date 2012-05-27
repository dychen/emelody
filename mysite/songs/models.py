from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Producer(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Artist(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class FeaturedArtist(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist)
    featured_artists = models.ManyToManyField(FeaturedArtist, blank=True)
    producer = models.ForeignKey(Producer, blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']

class Rating(models.Model):
    username = models.ForeignKey(User)
    song = models.ForeignKey(Song)
    rating = models.PositiveIntegerField()

class RecommendedSong(models.Model):
    username = models.ForeignKey(User)
    song = models.ForeignKey(Song)
    predicted_rating = models.DecimalField(max_digits=10, decimal_places=9)

class RecommendedArtist(models.Model):
    username = models.ForeignKey(User)
    artist = models.ForeignKey(Artist)
    count = models.PositiveIntegerField()

class SimilarUser(models.Model):
    username = models.ForeignKey(User, related_name='original_user')
    similar_user = models.ForeignKey(User, related_name='similar_user')
    score = models.DecimalField(max_digits=13, decimal_places=9)

class SimilarSong(models.Model):
    song = models.ForeignKey(Song, related_name='original_song')
    similar_song = models.ForeignKey(Song, related_name='similar_song')
    score = models.DecimalField(max_digits=13, decimal_places=9)

class Playlist(models.Model):
    username = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    song = models.ForeignKey(Song)

class Location(models.Model):
    username = models.ForeignKey(User)
    STATE_CHOICES = (
                     ('AL', 'Alabama'),
                     ('AK', 'Alaska'),
                     ('AZ', 'Arizona'),
                     ('AR', 'Arkansas'),
                     ('CA', 'California'),
                     ('CO', 'Colorado'),
                     ('CT', 'Connecticut'),
                     ('DE', 'Delaware'),
                     ('FL', 'Florida'),
                     ('GA', 'Georgia'),
                     ('HI', 'Hawaii'),
                     ('ID', 'Idaho'),
                     ('IL', 'Illinois'),
                     ('IN', 'Indiana'),
                     ('IA', 'Iowa'),
                     ('KS', 'Kansas'),
                     ('KY', 'Kentucky'),
                     ('LA', 'Louisiana'),
                     ('ME', 'Maine'),
                     ('MD', 'Maryland'),
                     ('MA', 'Massachusetts'),
                     ('MI', 'Michigan'),
                     ('MN', 'Minnesota'),
                     ('MS', 'Mississippi'),
                     ('MO', 'Missouri'),
                     ('MT', 'Montana'),
                     ('NE', 'Nebraska'),
                     ('NV', 'Nevada'),
                     ('NH', 'New Hampshire'),
                     ('NJ', 'New Jersey'),
                     ('NM', 'New Mexico'),
                     ('NY', 'New York'),
                     ('NC', 'North Carolina'),
                     ('ND', 'North Dakota'),
                     ('OH', 'Ohio'),
                     ('OK', 'Oklahoma'),
                     ('OR', 'Oregon'),
                     ('PA', 'Pennsylvania'),
                     ('RI', 'Rhode Island'),
                     ('SC', 'South Carolina'),
                     ('SD', 'South Dakota'),
                     ('TN', 'Tennessee'),
                     ('TX', 'Texas'),
                     ('UT', 'Utah'),
                     ('VT', 'Vermont'),
                     ('VA', 'Virginia'),
                     ('WA', 'Washington'),
                     ('WV', 'West Virginia'),
                     ('WI', 'Wisconsin'),
                     ('WY', 'Wyoming'),
                     )
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
