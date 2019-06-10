from __future__ import unicode_literals

from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin


from mezzanine.core.views import direct_to_template


admin.autodiscover()


urlpatterns = i18n_patterns(

    url("^admin/", include(admin.site.urls)),
    #url(r'^toidautu/giaodichNN/', include('GDNN.urls',namespace='giaodichNN',app_name='GDNN')),
    #url(r'^toidautu/thongtinvimo/', include('Vimo.urls',namespace='thongtinvimo',app_name='Vimo')),
    #url(r'^toidautu/', include('DexuatGD.urls',namespace='nhandinhthitruong',app_name='DexuatGD')),
    url(r'^auth/',include('social_django.urls', namespace='social')),
    url(r'^auth/', include('django.contrib.auth.urls', namespace='auth'))
               )
urlpatterns += [

    url("^$", direct_to_template, {"template": "index.html"}, name="home"),

    url("^", include("mezzanine.urls")),


]
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
