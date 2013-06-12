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
    #has_friends = models.ManyToManyField(UserProfile, related_name='is_friend_of')
    user1 = models.ForeignKey(UserProfile, related_name="user1")
    user2 = models.ForeignKey(UserProfile, related_name="user2")

    class Meta:
        unique_together = ('user1', 'user2')

    def __unicode__(self):
        return "%s %s" % (self.user1.user.username, self.user2.user.username)
  


class Osada(models.Model):
    nazwa = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, editable=False)
    user = models.OneToOneField(UserProfile)
    #budzet = models.IntegerField(null=True, default=8000)
    zloto = models.IntegerField(null=True, default=150)
    drewno = models.IntegerField(default=500)
    kamien = models.IntegerField(default=350)
    zelazo = models.IntegerField(default=270)
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


class Handel(models.Model):
    ZASOBY = (
        ('zloto', 'Zloto'),
        ('drewno', 'Drewno'),
        ('kamien', 'Kamien'),
        ('zelazo', 'Zelazo'),
    )

    osada = models.ForeignKey(Osada)
    surowiec1 = models.CharField("oferuje", max_length=10, blank=False, choices=ZASOBY, default='z')
    ilosc1 = models.IntegerField("w ilosci")
    surowiec2 = models.CharField("w zamian za", max_length=10, blank=False, choices=ZASOBY, default='z')
    ilosc2 = models.IntegerField("w ilosci")

    def __unicode__(self):
        return "%s %s %s" % (self.osada.nazwa, self.surowiec1, self.surowiec2)



class Budynki(models.Model):
    nazwa = models.CharField(max_length=120)
    slug = models.SlugField(max_length=130, null=True, editable=False)    
    koszt = models.IntegerField()    
    zloto = models.IntegerField()
    drewno = models.IntegerField()
    kamien = models.IntegerField()
    zelazo = models.IntegerField()
    produktywnosc = models.IntegerField()    
    jednostka_prod = models.CharField(max_length=30, null=True, blank=True)
    max_pojemnosc = models.IntegerField()
    max_level = models.IntegerField()

    def __unicode__(self):
        return "%s" % (self.nazwa)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nazwa)
        super(Budynki, self).save(*args, **kwargs)   

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
    produkcja = models.IntegerField(null=True, default=0)    
    max_pojemnosc = models.IntegerField(null=True, default=0)

    def __unicode__(self):
        return "%s" % (self.budynek.nazwa)  

    # posredniczaco odwolujemy sie do tabel Osady(pobrac nazwe usera) i Budynki(slug field)
    @models.permalink
    def get_absolute_url(self):
        return('utworz_obiekt', (), {
            'nazwa_profilu': self.osada.user,
            'kategoria': 'budynki',
            'slug': self.budynek.slug,
            'id': self.id,
            })


class Armia(models.Model):
    nazwa = models.CharField(max_length=120)
    budynek = models.ForeignKey(Budynki)
    slug = models.SlugField(max_length=130, null=True, editable=False)
    koszt = models.IntegerField(null=True, blank=True)
    atak = models.IntegerField()
    obrona = models.IntegerField()
    zbroja = models.IntegerField()
    zloto = models.IntegerField()
    drewno = models.IntegerField()
    kamien = models.IntegerField()
    zelazo = models.IntegerField()

    def __unicode__(self):
        return "%s" % (self.nazwa)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nazwa)
        super(Armia, self).save(*args, **kwargs)


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

    @models.permalink
    def get_absolute_url(self):
        return('utworz_obiekt', (), {
            'nazwa_profilu': self.osada.user,
            'kategoria': 'armia',
            'slug': self.armia.slug,
            'id': self.id,
            })

