from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import AuthenticateForm, UserCreateForm, OsadaForm
from django.core.urlresolvers import reverse
from .models import Osada, OsadaObiekt, Obiekt, UserProfile, Invites, Friends, Armia, Armia_osada, Budynki, Budynki_osada
from django.db.models import F
from django.contrib.auth.decorators import login_required

def index(request, auth_form=None, user_form=None):
    # User is logged
    
    if request.user.is_authenticated():        
        user = request.user        

        osada = Osada.objects.filter(user=request.user.profile)
        if osada:
            osada = osada[0]    

        
        """return render(request, 
                      "lpp_app/profil.html",
                      {'user': user, 'next_url': '/', 'osada': osada, })    
        """
        return render(request, 
                      "lpp_app/home.html",
                      {'user': user, 'next_url': '/', 'osada': osada, })    
        
        #return profil(request)

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
            return redirect('/')
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
    osada = Osada.objects.filter(user=request.user.profile)[0]

    armia = Armia_osada.objects.select_related().filter(osada=osada, ilosc__gt=0).order_by('-armia__nazwa')
    budynki = Budynki_osada.objects.select_related().filter(osada=osada, ilosc__gt=0).order_by('-budynek__nazwa')

    if request.POST.has_key('counter'):            
      budynki.filter(budynek__nazwa=request.POST['obiekt_nazwa']).update(
        produkcja=int(request.POST['counter'].split(' ')[0]) 
        )      

    return render(request,
                  "lpp_app/osada.html",
                  {'osada': osada,
                   'armia': armia,
                   'budynki': budynki,
                  })   


@login_required
def obiekty(request, nazwa_profilu=None, kategoria=None, utworzony_obiekt=None, brak_zasobow=False):
    osada = Osada.objects.filter(user=request.user.profile)[0]        
    print 'obiekt: ', kategoria

    if kategoria.startswith('armia'):   # startswitch bo zwraca URL=/armia/kup/rycerz-srebrny,2         
        armia = Armia_osada.objects.select_related().filter(osada=osada).order_by('-armia__zloto')

        return render(request,
                      "lpp_app/armia.html",
                      {'osada': osada, 'armia': armia, 
                      'utworzony_obiekt': utworzony_obiekt, 
                      'brak_zasobow': brak_zasobow, })
    elif kategoria.startswith('budynki'):
        budynki = Budynki_osada.objects.select_related().filter(osada=osada).order_by('-budynek__zloto')

        return render(request,
                      "lpp_app/budynki.html",
                      {'osada': osada, 'budynki': budynki, 
                      'utworzony_obiekt': utworzony_obiekt, 
                      'brak_zasobow': brak_zasobow, })
    else:        
        return redirect(reverse('osada'))
    """
    elif kategoria.startswith('mieszkancy'):
        # TODO: zmienic kategorie Mieszkancy na Ludnosc
        mieszkancy = [ob for ob in obiekty if ob.obiekt.kategoria.nazwa == 'Mieszkancy']

        return render(request,
                      "lpp_app/ludnosc.html",
                      {'osada': osada, 'mieszkancy': mieszkancy, 
                      'utworzony_obiekt': utworzony_obiekt, 
                      'brak_zasobow': brak_zasobow, })
    elif kategoria.startswith('zasoby'):
        zasoby = [ob for ob in obiekty if ob.obiekt.kategoria.nazwa == 'Zasoby']

        return render(request,
                      "lpp_app/zasoby.html",
                      {'osada': osada, 'zasoby': zasoby, 
                      'utworzony_obiekt': utworzony_obiekt, 
                      'brak_zasobow': brak_zasobow, })  
    """    


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
def friends(request, nazwa_profilu=None):
    #friends = Friends.objects.filter(user_from__user=request.user.profile)
    return render(request,
                  "lpp_app/friends.html")

@login_required
def market(request, nazwa_profilu=None):
    return render(request,
                  "lpp_app/market.html")

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

  # sprawdza czy zalogowany user zaprosil dana osade, 
  # zmienna invited okresla czy button "Zapros" bedzie widoczny
  # :user_from jest profilem dlatego request.user.profile
  # :user_to bierze osada.user ktora jest profilem
  if request.user.profile == osada.user:  # swoj profil, nie wyswietlaj zapros
    invited = True
  elif Invites.objects.filter(user_from=request.user.profile, user_to=osada.user):
    invited = True  

  return render(request,
                "lpp_app/wizytowka.html",
                {'osada': osada,
                 'invited': invited,
                })
