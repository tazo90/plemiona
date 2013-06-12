from django.conf.urls import patterns, include, url

# kolejnosc urli ma znaczenie, bo np. gdy url "utworz_obiekt" jest za "obiekty" 
# to nie dziala, a jak jest przed to wywoluje odpowiednio widok

urlpatterns = patterns('lpp_app.views',    

    url(r'^(?P<nazwa_profilu>.+)/pojedynki/$', 'pojedynki', name='pojedynki'),
    url(r'^(?P<nazwa_profilu>.+)/handel/$', 'handel', name='handel'),
    url(r'^(?P<nazwa_profilu>.+)/spolecznosc/$', 'spolecznosc', name='spolecznosc'),
    url(r'^(?P<nazwa_profilu>.+)/edycja/$', 'edycja_profilu', name='edycja_profilu'),
    url(r'^(?P<nazwa_profilu>.+)/friends/$', 'friends', name='friends'),
    url(r'^(?P<nazwa_profilu>.+)/zaproszenia/$', 'zaproszenia', name='zaproszenia'),
    url(r'^(?P<nazwa_profilu>.+)/statystyki/$', 'statystyki', name='statystyki'),
    
    url(r'^(?P<nazwa_profilu>.+)/osada/$', 'osada', name='osada'),        
    url(r'^(?P<nazwa_profilu>.+)/osada/dodaj/$', 'nowa_osada', name='nowa_osada'),        
    url(r'^(?P<nazwa_profilu>.+)/osada/(?P<kategoria>.+)/utworz/(?P<slug>[-\w\d]+),(?P<id>\d+)/$', 'utworz_obiekt', name='utworz_obiekt'),

    url(r'^(?P<nazwa_profilu>.+)/invite/(?P<zapr_osoba>.+)/delete/$', 'invite_delete', name='invite_delete'),
    url(r'^(?P<nazwa_profilu>.+)/invite/(?P<zapr_osoba>.+)/$', 'invite', name='invite'),        

    url(r'^(?P<nazwa_osady>.+)/osada/wizytowka/$', 'wizytowka', name='wizytowka'),

    # sa na koncu zeby odpowiednie url'e mogly dopasowac sie wczesniej
    url(r'^(?P<nazwa_profilu>.+)/osada/(?P<kategoria>.+)/$', 'obiekty', name='obiekty'),    
    url(r'^(?P<nazwa_profilu>.+)/$', 'profil', name='profil'),    
)
