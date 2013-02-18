from django.conf.urls import patterns, include, url
from foodtrucks import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^send_hipchat_notification', views.send_hipchat_notification, name='send_hipchat_notification'),
    url(r'^poll_food_trucks', views.poll_food_trucks, name='poll_food_trucks'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
