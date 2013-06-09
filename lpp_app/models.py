from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

class UserProfile(models.Model):

    def url(self, filename):
        path = "/Users/%s/%s" % (self.user.username, filename)
        return path

    user = models.OneToOneField(User)    
    avatar = models.ImageField(upload_to=url, blank=True)    

    def __unicode__(self):
        return self.user.username


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Invites(models.Model):
    user_from = models.ForeignKey(UserProfile, related_name='invites')
    user_to = models.ForeignKey(UserProfile, related_name='invited')

    class Meta:
        unique_together = ('user_from', 'user_to')

    def __unicode__(self):
        return "%s %s" % (self.user_from.user.username, self.user_to.user.username)



class Friends(models.Model):
    has_friends = models.ManyToManyField(UserProfile, related_name='is_friend_of')


class Osada(models.Model):
    nazwa = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, editable=False)
    user = models.OneToOneField(UserProfile)
    #budzet = models.IntegerField(null=True, default=8000)
    zloto = models.IntegerField(null=True, default=10)
    drewno = models.IntegerField(default=200)
    kamien = models.IntegerField(default=300)
    zelazo = models.IntegerField(default=80)
    rozwoj = models.IntegerField(null=True, default=2)
    data_powstania = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('nazwa',)

    def __unicode__(self):
        return self.nazwa

    @models.permalink
    def get_absolute_url(self):
        return ('osada', (), {
            'nazwa_profilu': self.user,
            })        

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nazwa)
        super(Osada, self).save(*args, **kwargs)


class Budynki(models.Model):
    nazwa = models.CharField(max_length=120)
    koszt = models.IntegerField()    
    zloto = models.IntegerField()
    drewno = models.IntegerField()
    kamien = models.IntegerField()
    zelazo = models.IntegerField()
    produktywnosc = models.IntegerField()    
    max_pojemnosc = models.IntegerField()
    max_poziom = models.IntegerField()

    def __unicode__(self):
        return "%s" % (self.nazwa)    

class Budynki_osada(models.Model):
    osada = models.ForeignKey(Osada, null=True, blank=True)
    budynek = models.ForeignKey(Budynki, null=True, blank=True)
    poziom = models.IntegerField(null=True, default=1)
    ilosc = models.IntegerField(null=True, default=0)    
    zloto = models.IntegerField(null=True, default=0)
    drewno = models.IntegerField(null=True, default=0)
    kamien = models.IntegerField(null=True, default=0)
    zelazo = models.IntegerField(null=True, default=0)
    produktywnosc = models.IntegerField(null=True, default=0)
    max_pojemnosc = models.IntegerField(null=True, default=0)

    def __unicode__(self):
        return "%s" % (self.budynek.nazwa)

class Armia(models.Model):
    nazwa = models.CharField(max_length=120)
    koszt = models.IntegerField()
    atak = models.IntegerField()
    obrona = models.IntegerField()
    zbroja = models.IntegerField()
    zloto = models.IntegerField()
    drewno = models.IntegerField()
    kamien = models.IntegerField()
    zelazo = models.IntegerField()

    def __unicode__(self):
        return "%s" % (self.nazwa)


class Armia_osada(models.Model):    
    osada = models.ForeignKey(Osada, null=True, blank=True)
    armia = models.ForeignKey(Armia, null=True, blank=True)    
    poziom = models.IntegerField(null=True, default=1)
    ilosc = models.IntegerField(null=True, default=0)
    zloto = models.IntegerField(null=True, default=0)
    drewno = models.IntegerField(null=True, default=0)
    kamien = models.IntegerField(null=True, default=0)
    zelazo = models.IntegerField(null=True, default=0)

    def __unicode__(self):
        return "%s" % (self.armia.nazwa)


class Kategoria(models.Model):
    nazwa = models.CharField(max_length=50)
    url = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return self.nazwa


class Obiekt(models.Model):
    nazwa = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, editable=False)
    kategoria = models.ForeignKey(Kategoria)    
    cena = models.IntegerField() 
    poczatkowa_ilosc = models.IntegerField(null=True, default=0)       
    max_ilosc = models.IntegerField()    

    def __unicode__(self):
        return self.nazwa

    @models.permalink
    # skrot od: {% url kup ar.obiekt.slug ar.obiekt.id %}
    def get_absolute_url(self):
        return ('kup', (), {    
            'nazwa_profilu': 'test-usunac',                
            'kategoria': unicode(self.kategoria).lower(),
            'slug': self.slug,
            'id': self.id,
            })

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nazwa)
        super(Obiekt, self).save(*args, **kwargs)

#Osada.obiekty = property(lambda u: Obiekt.objects.get_or_create(osada=u))

class OsadaObiekt(models.Model):
    osada = models.ForeignKey(Osada)
    obiekt = models.ForeignKey(Obiekt)
    ilosc = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        unique_together = ("osada", "obiekt")

    def __unicode__(self):
        return u'%s %s' % (self.osada.nazwa, self.obiekt.nazwa)
