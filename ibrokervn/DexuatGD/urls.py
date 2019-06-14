from __future__ import unicode_literals
from mezzanine.conf import settings

_slash = "/" if settings.APPEND_SLASH else ""


from django.conf.urls import url
from DexuatGD import views


app_name='DexuatGD'
urlpatterns = [
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
        views.stock_detail,
        name='phantichcophieu'),
    url(r'^tonghopthongtin/', views.Tonghopthongtin, name='tonghopthongtin'),
    url(r'^import_Doanhnghiep/', views.import_Stock_basic_info , name='import'),
    url("^tag/(?P<tag>.*)%s$" % _slash,
        views.Nhandinh_list, name="NhandinhTT_DexuatGD_list_tag"),
    url("^category/(?P<category>.*)%s$" % _slash,
        views.Nhandinh_list, name="NhandinhTT_DexuatGD_list_category"),
    url("^author/(?P<username>.*)%s$" % _slash,
        views.Nhandinh_list, name="NhandinhTT_DexuatGD_list_author"),
    url("^archive/(?P<year>\d{4})/(?P<month>\d{1,2})%s$" % _slash,
        views.Nhandinh_list, name="NhandinhTT_DexuatGD_list_month"),
    url("^archive/(?P<year>\d{4})%s$" % _slash,
        views.Nhandinh_list, name="NhandinhTT_DexuatGD_list_year"),
    url("^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/"
        "(?P<slug>.*)%s$" % _slash,
        views.Nhandinh_detail, name="Nhandinh_detail_day"),
    url("^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>.*)%s$" % _slash,
        views.Nhandinh_detail, name="Nhandinh_detail_month"),
    url("^(?P<year>\d{4})/(?P<slug>.*)%s$" % _slash,
        views.Nhandinh_detail, name="Nhandinh_detail_year"),
    url("^nhandinhmoinhat%s$" % _slash, views.Nhandinh_detail_moinhat, name='newest'),
    url("^(?P<slug>.*)%s$" % _slash, views.Nhandinh_detail, name='daily'),
    url("^$", views.Nhandinh_list, name="NhandinhTT_DexuatGD_list"),
      ]
