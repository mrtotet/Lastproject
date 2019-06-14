from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from .models import Vimo,Viewed
# Create your views here.
def Vimo_list(request):
    Post60 = Vimo.objects.filter(status='published').order_by('-publish')[0:60]

    views = get_object_or_404(Viewed)
    views.viewed_list_Vimo +=1
    views.save()

    context = {'Post60':Post60,'views':views,
                 }
    template = "pages/toidautu/thongtinvimo.html"
    return render(request,template,context)


