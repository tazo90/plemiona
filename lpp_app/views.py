from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import AuthenticateForm, UserCreateForm, OsadaForm
from django.core.urlresolvers import reverse
from .models import Osada, OsadaObiekt, Obiekt
from django.db.models import F

def index(request, auth_form=None, user_form=None):
    # User is logged
    if request.user.is_authenticated():        
        user = request.user        

        osada = Osada.objects.filter(user=request.user.profile)
        if osada:
            osada = osada[0]    
        
        return render(request, 
                      "lpp_app/profile.html",
                      {'user': user, 'next_url': '/', 'osada': osada, })    
    else:
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()

        return render(request,
                     "lpp_app/home.html",
                     {'auth_form': auth_form, })


def login_view(request):
    if request.method == 'POST':        
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect('/')
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
            return redirect('/')
        else:
            return signup(request, user_form=user_form)

    user_form = user_form or UserCreateForm()
    auth_form = auth_form or AuthenticateForm()    
    return render(request,
                  "lpp_app/signup.html",
                  {'user_form': user_form, 'auth_form': auth_form, })    


def nowa_osada(request, osada_form=None):    
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


def osada(request):
    osada = Osada.objects.filter(user=request.user.profile)[0]

    # pobierz obiekty
    armia = []    
    budynki = []
    mieszkancy = []
    zasoby = []

    obiekty = OsadaObiekt.objects.select_related().filter(osada=osada)

    for ob in obiekty:
        if ob.obiekt.kategoria.nazwa == 'Armia':
            armia.append(ob)
        elif ob.obiekt.kategoria.nazwa == 'Budynki':
            budynki.append(ob)
        elif ob.obiekt.kategoria.nazwa == 'Mieszkancy':
            mieszkancy.append(ob)
        else:
            zasoby.append(ob)

    return render(request,
                 "lpp_app/osada.html",
                 {'osada': osada, 
                  'armia': armia,
                  'budynki': budynki,
                  'mieszkancy': mieszkancy,
                  'zasoby': zasoby,
                 })


def obiekty(request, kategoria='', kupiony_obiekt=None, brak_srodkow=False):
    osada = Osada.objects.filter(user=request.user.profile)[0]
    obiekty = OsadaObiekt.objects.select_related().filter(osada=osada).order_by('-obiekt__cena')        

    if kategoria.startswith('armia'):   # startswitch bo zwraca URL=/armia/kup/rycerz-srebrny,2         
        armia = [ob for ob in obiekty if ob.obiekt.kategoria.nazwa == 'Armia']

        return render(request,
                      "lpp_app/armia.html",
                      {'osada': osada, 'armia': armia, 
                      'kupiony_obiekt': kupiony_obiekt, 
                      'brak_srodkow': brak_srodkow, })
    elif kategoria.startswith('budynki'):
        budynki = [ob for ob in obiekty if ob.obiekt.kategoria.nazwa == 'Budynki']

        return render(request,
                      "lpp_app/budynki.html",
                      {'osada': osada, 'budynki': budynki, 
                      'kupiony_obiekt': kupiony_obiekt, 
                      'brak_srodkow': brak_srodkow, })
    elif kategoria.startswith('mieszkancy'):
        # TODO: zmienic kategorie Mieszkancy na Ludnosc
        mieszkancy = [ob for ob in obiekty if ob.obiekt.kategoria.nazwa == 'Mieszkancy']

        return render(request,
                      "lpp_app/ludnosc.html",
                      {'osada': osada, 'mieszkancy': mieszkancy, 
                      'kupiony_obiekt': kupiony_obiekt, 
                      'brak_srodkow': brak_srodkow, })
    elif kategoria.startswith('zasoby'):
        zasoby = [ob for ob in obiekty if ob.obiekt.kategoria.nazwa == 'Zasoby']

        return render(request,
                      "lpp_app/zasoby.html",
                      {'osada': osada, 'zasoby': zasoby, 
                      'kupiony_obiekt': kupiony_obiekt, 
                      'brak_srodkow': brak_srodkow, })
    else:        
        return redirect(reverse('osada'))



def kup(request, kategoria, slug, id):
    osada = Osada.objects.get(user=request.user)
    kupiony_obiekt = Obiekt.objects.get(pk=id)        
    brak_srodkow = False

    # pobranie kategorii z ktorej kupilismy obiekt, potrzebne w metodzie obiekt aby
    # poinformowac w ktorej kategorii zostac
    kategoria = unicode(kupiony_obiekt.kategoria.nazwa).lower() 

    # aktualizacja krotek funkcja F
    if osada.budzet > kupiony_obiekt.cena:           
        OsadaObiekt.objects.filter(osada=osada, obiekt=kupiony_obiekt).update(ilosc=F('ilosc')+1) 
        Osada.objects.filter(user=request.user).update(budzet=F('budzet')-kupiony_obiekt.cena)                
        
        # zwieksz calkowity postep
        if kupiony_obiekt.kategoria.id == 1:    # armia
            Osada.objects.filter(user=request.user).update(rozwoj=F('rozwoj')+1)                
        elif kupiony_obiekt.kategoria.id == 2:    # budynki
            Osada.objects.filter(user=request.user).update(rozwoj=F('rozwoj')+5)
        elif kupiony_obiekt.kategoria.id == 3:    # mieszkancy
            Osada.objects.filter(user=request.user).update(rozwoj=F('rozwoj')+2)
        elif kupiony_obiekt.kategoria.id == 4:    # zasoby
            Osada.objects.filter(user=request.user).update(rozwoj=F('rozwoj')+1)
    else:                
        kupiony_obiekt = [] 
        brak_srodkow = True        

    # po kupnie pozostan na tej samej stronie (kategorii)   
    return obiekty(request, kategoria, kupiony_obiekt, brak_srodkow)
