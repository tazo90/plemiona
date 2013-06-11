from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lpp.views.home', name='home'),
    # url(r'^lpp/', include('lpp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'lpp_app.views.index', name='index'),
    url(r'login$', 'lpp_app.views.login_view', name='login'),
    url(r'logout$', 'lpp_app.views.logout_view', name='logout'),        
    url(r'signup$', 'lpp_app.views.signup', name='signup'),    

    url(r'', include('lpp_app.urls')),
)
