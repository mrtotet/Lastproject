from django.conf.urls import url

from django.conf.urls.i18n import i18n_patterns
from GDNN import views

app_name='GDNN'
urlpatterns = i18n_patterns (
    url(r'import_GDNN',views.import_GDNN, name='import_gdnn'),
    url(r'$',views.TKgdnn, name='gdnn'),

)

