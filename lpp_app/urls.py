from django.conf.urls import patterns, include, url

urlpatterns = patterns('lpp_app.views',
    url('^$', 'index', name='index'),
)
