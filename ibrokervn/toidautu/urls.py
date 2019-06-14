from django.conf.urls import url
from Main import views


app_name='Main'
urlpatterns = [
    url(r'chienluocgiaodich$', views.Trading_strategy , name='index'),
      ]