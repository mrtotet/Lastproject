from django.conf.urls import url
from Vimo import views
from django.conf.urls.i18n import i18n_patterns





app_name='Vimo'
urlpatterns = i18n_patterns (


    url(r'^$',views.Vimo_list, name='vimo'),

)


