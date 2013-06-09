from django.conf.urls import patterns, include, url

urlpatterns = patterns('lpp_app.views',    

    url(r'^(?P<nazwa_profilu>.+)/edycja$', 'edycja_profilu', name='edycja_profilu'),
    url(r'^(?P<nazwa_profilu>.+)/friends$', 'friends', name='friends'),
    url(r'^(?P<nazwa_profilu>.+)/zaproszenia$', 'zaproszenia', name='zaproszenia'),
    url(r'^(?P<nazwa_profilu>.+)/statystyki$', 'statystyki', name='statystyki'),
    url(r'^(?P<nazwa_profilu>.+)/osada$', 'osada', name='osada'),
    url(r'^(?P<nazwa_profilu>.+)/osada/dodaj$', 'nowa_osada', name='nowa_osada'),    
    url(r'^(?P<nazwa_profilu>.+)/osada/(?P<kategoria>.+)/$', 'obiekty', name='obiekty'),    
    url(r'^(?P<nazwa_profilu>.+)/osada/(?P<kategoria>.+)/kup/(?P<slug>[-\w\d]+),(?P<id>\d+)/$', 'kup', name='kup'),
    url(r'^(?P<nazwa_profilu>.+)/$', 'profil', name='profil'),    
)
