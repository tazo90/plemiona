#coding: utf-8
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.db.models import F, Q
from django.shortcuts import render, redirect

from .forms import AuthenticateForm, UserCreateForm, OsadaForm, HandelForm
from .models import Osada, Handel, UserProfile, Invites, Friends, Armia, Armia_osada, Budynki, Budynki_osada

def index(request, auth_form=None, user_form=None):
    # User is logged
    
    if request.user.is_authenticated():        
        user = request.user        

        osada = Osada.objects.filter(user=request.user.profile)
        if osada:
            osada = osada[0]    

        return render(request, 
                      "lpp_app/home.html",
                      {'user': user, 'next_url': '/', 'osada': osada, })                    

    else:    
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()

        return render(request,
                     "lpp_app/home.html",
                     {'auth_form': auth_form, })



def profil(request, nazwa_profilu=None):
    user = request.user
    osada = Osada.objects.filter(user=user.profile)    
    if osada:
        osada = osada[0]    

    return render(request,
                  "lpp_app/profil.html",
                  {'user': user, 'osada': osada, })



def login_view(request):
    if request.method == 'POST':        
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success, route to user profile
            return redirect(reverse('profil', args=(request.user.profile,) ))
        else:
            # Failure
            # route to specified url depending on url passed in POST
            view_name = request.POST.get('url')
            if view_name == 'index':
                return index(request, auth_form=form)
            elif view_name == 'register':
                return register(request, auth_form=form)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


def signup(request, auth_form=None, user_form=None):    
    if request.method == "POST":
        user_form = UserCreateForm(data=request.POST)
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('profil', args=(request.user.profile,)))
        else:
            return signup(request, user_form=user_form)

    user_form = user_form or UserCreateForm()
    auth_form = auth_form or AuthenticateForm()    
    return render(request,
                  "lpp_app/signup.html",
                  {'user_form': user_form, 'auth_form': auth_form, })    


@login_required
def edycja_profilu(request, nazwa_profilu=None):
  return render(request,
                "lpp_app/edycja_profilu.html")


@login_required
def nowa_osada(request, nazwa_profilu=None, osada_form=None):    
    if request.method == "POST":         
        osada_form = OsadaForm(data=request.POST)
        if osada_form.is_valid():
            osada = osada_form.save(commit=False)
            osada.user = request.user.profile
            osada.save()            
            return redirect(reverse('profil', args=(nazwa_profilu,)))
        else:
            return nowa_osada(request, osada_form=osada_form)
    
    osada_form = OsadaForm()
    return render(request, 
                 "lpp_app/utworz_osade.html", 
                 {'osada_form': osada_form, })        


from django.views.decorators.csrf import csrf_exempt
@login_required
@csrf_exempt
def osada(request, nazwa_profilu=None):            
    osada = Osada.objects.filter(user=request.user.profile)

    armia = Armia_osada.objects.select_related().filter(osada=osada[0], ilosc__gt=0).order_by('-armia__nazwa')
    budynki = Budynki_osada.objects.select_related().filter(osada=osada[0], ilosc__gt=0).order_by('-budynek__nazwa')

    if request.POST.has_key('counter'):                  
      if request.POST['obiekt_nazwa'] == u'Kopalnia złota':
        osada.update(zloto=F('zloto') + 30)
      elif request.POST['obiekt_nazwa'] == u'Kopalnia żelaza':
        osada.update(zelazo=F('zelazo') + 30)
      elif request.POST['obiekt_nazwa'] == u'Tartak':
        osada.update(drewno=F('drewno') + 30)
      elif request.POST['obiekt_nazwa'] == u'Kamieniołom':
        osada.update(kamien=F('kamien') + 30)

      budynki.filter(budynek__nazwa=request.POST['obiekt_nazwa']).update(
        produkcja=int(request.POST['counter'].split(' ')[0],) 
        )      

    return render(request,
                  "lpp_app/osada.html",
                  {'osada': osada[0],
                   'armia': armia,
                   'budynki': budynki,
                  })   


@login_required
def obiekty(request, nazwa_profilu=None, kategoria=None, utworzony_obiekt=None, brak_zasobow=False):
    osada = Osada.objects.filter(user=request.user.profile)[0]        

    if kategoria.startswith('armia'):   # startswitch bo zwraca URL=/armia/kup/rycerz-srebrny,2         
        armia = Armia_osada.objects.select_related().filter(osada=osada).order_by('armia__nazwa')

        return render(request,
                      "lpp_app/armia.html",
                      {'osada': osada, 'armia': armia, 
                      'utworzony_obiekt': utworzony_obiekt, 
                      'brak_zasobow': brak_zasobow, })
    elif kategoria.startswith('budynki'):
        budynki = Budynki_osada.objects.select_related().filter(osada=osada).order_by('budynek__nazwa')

        return render(request,
                      "lpp_app/budynki.html",
                      {'osada': osada, 'budynki': budynki, 
                      'utworzony_obiekt': utworzony_obiekt, 
                      'brak_zasobow': brak_zasobow, })
    else:        
        return redirect(reverse('osada'))

 


def utworz_obiekt(request, nazwa_profilu=None, kategoria=None, slug=None, id=None):  
  print 'kat: ', kategoria
  osada = Osada.objects.select_related().filter(user=request.user)
  utworzony_obiekt = None
  brak_zasobow = False

  if kategoria == 'armia':
    # bierze obiekt z podanej osady
    nowy_obiekt = Armia_osada.objects.select_related().filter(osada=osada[0], pk=id)
    utworzony_obiekt = nowy_obiekt[0].armia.nazwa
  elif kategoria == 'budynki':
    nowy_obiekt = Budynki_osada.objects.select_related().filter(osada=osada[0], pk=id)
    utworzony_obiekt = nowy_obiekt[0].budynek.nazwa


  if osada[0].zloto >= nowy_obiekt[0].zloto and \
    osada[0].drewno >= nowy_obiekt[0].drewno and \
    osada[0].kamien >= nowy_obiekt[0].kamien and \
    osada[0].zelazo >= nowy_obiekt[0].zelazo:
      # aktualizuj ilosc obiektu
      nowy_obiekt.update(ilosc=F('ilosc') + 1)
      # aktualna ilosc zlota = osada.zloto - nowy_obiekt.zloto, itd dla drewna,kamienia,zelaza
      osada.update(zloto=F('zloto') - nowy_obiekt[0].zloto, 
                   drewno=F('drewno') - nowy_obiekt[0].drewno,
                   kamien=F('kamien') - nowy_obiekt[0].kamien,
                   zelazo=F('zelazo') - nowy_obiekt[0].zelazo
                  )
      
  else:    
    utworzony_obiekt = None
    brak_zasobow = True

  # pozostan na tej samej stronie
  return obiekty(request, kategoria=kategoria, utworzony_obiekt=utworzony_obiekt, brak_zasobow=brak_zasobow)


@login_required
def spolecznosc(request, nazwa_profilu=None):    
    osady = Osada.objects.all()
    return render(request, 
                  "lpp_app/spolecznosc.html",
                  {'osady': osady,})

@login_required
def zaproszenia(request, nazwa_profilu=None):
    sent_invites = Invites.objects.filter(user_from__user=request.user)
    receive_invites = Invites.objects.filter(user_to__user=request.user)    
    
    osady1 = [Osada.objects.get(user=inv.user_to) for inv in sent_invites]
    osady2 = [Osada.objects.get(user=inv.user_from) for inv in receive_invites] 
    
    sent_invites = zip(sent_invites, osady1)
    receive_invites = zip(receive_invites, osady2)

    return render(request,
                  "lpp_app/zaproszenia.html",
                  {'sent_invites': sent_invites, 
                   'receive_invites': receive_invites,                   
                  })

@login_required
def invite(request, nazwa_profilu=None, zapr_osoba=None):
  u1 = UserProfile.objects.get(user=request.user)
  u2 = UserProfile.objects.get(user__username=zapr_osoba)    
  
  if not Invites.objects.filter(user_from=u1, user_to=u2):
    Invites.objects.create(user_from=u1, user_to=u2)      

  return redirect(reverse("zaproszenia", args=(nazwa_profilu,)))


@login_required
def invite_delete(request, nazwa_profilu=None, zapr_osoba=None):
  u1 = UserProfile.objects.get(user=request.user)  
  u2 = UserProfile.objects.get(user__username=zapr_osoba)

  Invites.objects.filter(user_from=u1, user_to=u2).delete()
  #gdu nie powoedzenie, to pewnie jest druga relacja
  Invites.objects.filter(user_from=u2, user_to=u1).delete()

  return redirect(reverse("zaproszenia", args=(nazwa_profilu,)))


@login_required
def invite_accept(request, nazwa_profilu=None, zapr_osoba=None):
  kto_zaprasza = UserProfile.objects.get(user__username=zapr_osoba)
  Friends.objects.create(user1=request.user.profile, user2=kto_zaprasza)

  Invites.objects.filter(user_from=request.user.profile, user_to=kto_zaprasza).delete()
  Invites.objects.filter(user_from=kto_zaprasza, user_to=request.user.profile).delete()
  return redirect(reverse('friends', args=(nazwa_profilu, )))
  

@login_required
def friends(request, nazwa_profilu=None):

    friends = Friends.objects.filter(
      Q(user1=request.user) | Q(user2=request.user)
    )
    
    """ bierze naszych wszystkich przyjacieli i wrzuca krotke do listy postaci (user,osada) """  
    res = []
    for friend in friends:
      if friend.user1 != request.user.profile:
        res.append( (friend.user1, Osada.objects.get(user=friend.user1)) )        
      elif friend.user2 != request.user.profile:
        res.append( (friend.user2, Osada.objects.get(user=friend.user2)) )        
        

    return render(request,
                  "lpp_app/friends.html",
                  {'friends': res,})

@login_required
def handel(request, nazwa_profilu=None):
    if request.method == "POST":         
        handel_form = HandelForm(data=request.POST)
        if handel_form.is_valid():
            _handel = handel_form.save(commit=False)
            _handel.osada = Osada.objects.get(user=request.user)
            _handel.save()            
            return redirect(reverse('handel', args=(nazwa_profilu,)))
        else:
            #return handel(request, handel_form=handel_form)
            #powinien wywolac handel zeby sprawdzic bledu w form
            return redirect(reverse('handel', args=(nazwa_profilu,)))
    
    handel_form = HandelForm()  
    oferta = Handel.objects.all()
    return render(request,
                  "lpp_app/handel.html",
                  {'handel_form': handel_form, 
                   'oferta': oferta,})


def wymiana(request, nazwa_profilu=None, sur1=None, ile1=None, sur2=None, ile2=None):
  #print sur1, ' ', ile1, ' ', sur2, ' ', ile2
  osada_sprzed = Osada.objects.filter(user__user__username=nazwa_profilu)
  osada_kupuj = Osada.objects.filter(user=request.user)   # TO MY!

  if sur2 == 'zloto':
    if osada_kupuj[0].zloto > int(ile2):    
      if sur1 == 'zloto':        
        osada_kupuj.update(zloto=F('zloto') + ile1 - ile2)
        osada_sprzed.update(zloto=F('zloto') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
      elif sur1 == 'drewno':
        osada_kupuj.update(zloto=F('zloto') - ile2, drewno=F('drewno') + ile1)
        osada_sprzed.update(zloto=F('zloto') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
      elif sur1 == 'kamien':
        osada_kupuj.update(zloto=F('zloto') - ile2, kamien=F('kamien') + ile1)
        osada_sprzed.update(zloto=F('zloto') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
      elif sur1 == 'zelazo':
        osada_kupuj.update(zloto=F('zloto') - ile2, zelazo=F('zelazo') + ile1)
        osada_sprzed.update(zloto=F('zloto') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
  elif sur2 == 'drewno':
    if osada_kupuj[0].drewno > int(ile2):    
      if sur1 == 'zloto':        
        osada_kupuj.update(drewno=F('drewno') - ile2, zloto=F('zloto') + ile1)
        osada_sprzed.update(drewno=F('drewno') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
      elif sur1 == 'drewno':
        osada_kupuj.update(drewno=F('drewno') + ile1 - ile2)
        osada_sprzed.update(drewno=F('drewno') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
      elif sur1 == 'kamien':
        osada_kupuj.update(drewno=F('drewno') - ile2, kamien=F('kamien') + ile1)
        osada_sprzed.update(drewno=F('drewno') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
      elif sur1 == 'zelazo':
        osada_kupuj.update(drewno=F('drewno') - ile2, zelazo=F('zelazo') + ile1)
        osada_sprzed.update(drewno=F('drewno') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
  elif sur2 == 'kamien':
    if osada_kupuj[0].kamien > int(ile2):    
      if sur1 == 'zloto':        
        osada_kupuj.update(kamien=F('kamien') - ile2, zloto=F('zloto') + ile1)
        osada_sprzed.update(kamien=F('kamien') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
      elif sur1 == 'kamien':
        osada_kupuj.update(kamien=F('kamien') + ile1 - ile2)
        osada_sprzed.update(kamien=F('kamien') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
      elif sur1 == 'drewno':
        osada_kupuj.update(kamien=F('kamien') - ile2, drewno=F('drewno') + ile1)
        osada_sprzed.update(kamien=F('kamien') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
      elif sur1 == 'zelazo':
        osada_kupuj.update(kamien=F('kamien') - ile2, zelazo=F('zelazo') + ile1)
        osada_sprzed.update(kamien=F('kamien') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
  elif sur2 == 'zelazo':
    if osada_kupuj[0].zelazo > int(ile2):    
      if sur1 == 'zloto':        
        osada_kupuj.update(zelazo=F('zelazo') - ile2, zloto=F('zloto') + ile1)
        osada_sprzed.update(zelazo=F('zelazo') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
      elif sur1 == 'zelazo':
        osada_kupuj.update(zelazo=F('zelazo') + ile1 - ile2)
        osada_sprzed.update(zelazo=F('zelazo') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
      elif sur1 == 'drewno':
        osada_kupuj.update(zelazo=F('zelazo') - ile2, drewno=F('drewno') + ile1)
        osada_sprzed.update(zelazo=F('zelazo') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()
      elif sur1 == 'kamien':
        osada_kupuj.update(zelazo=F('zelazo') - ile2, kamien=F('kamien') + ile1)
        osada_sprzed.update(zelazo=F('zelazo') + ile2)
        Handel.objects.filter(osada=osada_sprzed[0], surowiec1=sur1, ilosc1=ile1, surowiec2=sur2, ilosc2=ile2).delete()

  return redirect(reverse('handel', args=(nazwa_profilu, )))



@login_required
def pojedynki(request, nazwa_profilu=None):
  return render(request,
                "lpp_app/pojedynki.html")

@login_required
def statystyki(request, nazwa_profilu=None):
  return render(request,
               "lpp_app/statystyki.html")


@login_required
def wizytowka(request, nazwa_osady=None):  
  osada = Osada.objects.select_related().get(nazwa=nazwa_osady)    
  invited = False

  """
    sprawdza czy zalogowany user zaprosil dana osade, 
    zmienna invited okresla czy button "Zapros" bedzie widoczny
    :user_from jest profilem dlatego request.user.profile
    :user_to bierze osada.user ktora jest profilem
  """
  if request.user.profile == osada.user:  # swoj profil, nie wyswietlaj zapros
    invited = True
  elif Invites.objects.filter(user_from=request.user.profile, user_to=osada.user):
    invited = True    
  elif Friends.objects.filter(user1=request.user.profile, user2=osada.user) or Friends.objects.filter(user1=osada.user, user2=request.user.profile):
    invited = True
  
  return render(request,
                "lpp_app/wizytowka.html",
                {'osada': osada,
                 'invited': invited,
                })
