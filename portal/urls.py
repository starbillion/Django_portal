from django.conf.urls import url
from django.urls import path, include

from . import views

urlpatterns = [
    # entry point
    url(r'^$', views.index, name='index'),
    url(r'accounts/login/$', views.index, name='index'),
    # subscription routing
    url(r'^subscription/$', views.subscription, name='subscription'),

    # payment result routing
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^success/$', views.payment_success, name='success'),
    url(r'^failed/$', views.payment_failed, name='failed'),

    # farm level importing routing
    url(r'^import_farmlevel/$', views.import_farmlevel, name='import_farmlevel'),

    # portal form kind routing
        url(r'^form1/$', views.form1, name='form1'),
    url(r'^form2/$', views.form2, name='form2'),
    url(r'^form3/$', views.form3, name='form3'),
    url(r'^form4/$', views.form4, name='form4'),
    # routing of profile page
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/fblist/$', views.fblist, name='fblist'),
    url(r'^profile/add_fb/$', views.add_fb, name='add_fb'),
    url(r'^profile/validate_fb/$', views.validate_fb, name='validate_fb'),
    url(r'^profile/update_fb/$', views.update_fb, name='update_fb'),
    url(r'^profile/get_fb_key/$', views.get_fb_key, name='get_fb_key'),

    # routing of form script
    url(r'^start_form1/$', views.start_form1, name='start_form1'),
    url(r'^start_form2/$', views.start_form2, name='start_form2'),
    url(r'^start_form3/$', views.start_form3, name='start_form3'),
    url(r'^start_form4/$', views.start_form4, name='start_form4'),
    # running custom script
    url(r'^running_result_form1/$', views.running_result_form1, name='running_result_form1'),

    # stop custom script
    url(r'^script_stop/$', views.script_stop, name='script_stop'),

    url(r'^tasks/$', views.tasks, name='tasks'),
    # routing set up for login/register
    url(r'^ajax/login/$', views.login, name='login'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^ajax/validate_email/$', views.validate_email, name='validate_email'),
    url(r'^ajax/forget_email/$', views.forget_email, name='forget_email'),
    url(r'^ajax/register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
]
