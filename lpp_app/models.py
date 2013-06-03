from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class UserProfile(models.Model):

    def url(self, filename):
        path = "/Users/%s/%s" % (self.user.username, filename)
        return path

    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to=url, blank=True)    

    def __unicode__(self):
        return self.user.username


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Osada(models.Model):
    nazwa = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, editable=False)
    user = models.OneToOneField(UserProfile)
    budzet = models.IntegerField(null=True, default=8000)
    rozwoj = models.IntegerField(null=True, default=2)
    data_powstania = models.DateTimeField(auto_now_add=True)    

    def __unicode__(self):
        return self.nazwa

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nazwa)
        super(Osada, self).save(*args, **kwargs)


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
