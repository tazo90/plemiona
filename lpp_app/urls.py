from django.conf.urls import patterns, include, url

urlpatterns = patterns('lpp_app.views',
    url(r'^$', 'index', name='index'),
    url(r'^login$', 'login_view', name='login'),
    url(r'^logout$', 'logout_view', name='logout'),        
    url(r'^signup$', 'signup', name='signup'),
    url(r'^osada$', 'osada', name='osada'),
    url(r'^osada/dodaj$', 'nowa_osada', name='nowa_osada'),
    url(r'^osada/(?P<kategoria>.+)/kup/(?P<slug>[-\w\d]+),(?P<id>\d+)/$', 'kup', name='kup'),
    url(r'^osada/(?P<kategoria>.+)/$', 'obiekty', name='obiekty'),
    #url(r'^osada/armia$', 'armia', name='armia'),    
)
