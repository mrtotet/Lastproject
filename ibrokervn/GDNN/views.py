from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django import forms
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
import django_excel as excel
from .models import GDNN, Viewed
from django.contrib.admin.views.decorators import staff_member_required

data =[1, 2, 3]
class UploadFileForm(forms.Form):
    file = forms.FileField()

@staff_member_required
def import_GDNN(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            request.FILES['file'].save_to_database(
                name_columns_by_row=0,
                model=GDNN,
                mapdict=[   'pub_date',
                            'Vol_Mua' ,
                            'Val_Mua' ,
                            'Vol_Ban' ,
                            'Val_Ban' ,
                            'Vol_Rong',
                            'Val_Rong',
                            'Vol_Mua_KL',
                            'Val_Mua_KL',
                            'Vol_Ban_KL',
                            'Val_Ban_KL',

                            'Val_KL_Rong',

                            'Vol_Mua_TT',
                            'Val_Mua_TT',
                            'Vol_Ban_TT',
                            'Val_Ban_TT',

                            'Val_TT_Rong',

                            'Room_NN_hientai',
                            'Total_Room_NN',
                            'Phantram_tong_SH_NN',
                            'SH_NN',
                            'Phantram_SH_NN',

                            ]
            )
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    template = "pages/toidautu/giaodichNN/import_GDNN.html"
    context = {'form': form}

    return render(
        request,
        template,
        context)

from django.db.models import Sum


from .models import GDNN, Viewed
# Create your views here.

def TKgdnn(request):
    Name = [f for f in GDNN._meta.get_fields() if f.name != 'id' if f.name != 'status']
    Post = GDNN.objects.filter(status='published')
    Post5 = Post.order_by('-pub_date')[:5]
    Post20 = Post.order_by('-pub_date')[:20]
    Post40 = Post.order_by('-pub_date')[:40]
    Post60 = Post.order_by('-pub_date')[0:60]
    GTGDRong5days =    Post5.aggregate(total=Sum('Val_Rong'))
    GTGDRong20days =   Post20.aggregate(total=Sum('Val_Rong'))
    GTGDRong40days =   Post40.aggregate(total=Sum('Val_Rong'))
    GTGDRong60days =   Post60.aggregate(total=Sum('Val_Rong'))
    GTGDKLRong5days =  Post5.aggregate(total=Sum('Val_KL_Rong'))
    GTGDKLRong20days = Post20.aggregate(total=Sum('Val_KL_Rong'))
    GTGDKLRong40days = Post40.aggregate(total=Sum('Val_KL_Rong'))
    GTGDKLRong60days = Post60.aggregate(total=Sum('Val_KL_Rong'))
    GTGDTTRong5days =  Post5.aggregate(total=Sum('Val_TT_Rong'))
    GTGDTTRong20days = Post20.aggregate(total=Sum('Val_TT_Rong'))
    GTGDTTRong40days = Post40.aggregate(total=Sum('Val_TT_Rong'))
    GTGDTTRong60days = Post60.aggregate(total=Sum('Val_TT_Rong'))

    views = get_object_or_404(Viewed)
    views.viewed_gdnn +=1
    views.save()

    template = "pages/toidautu/giaodichNN.html"
    context = { 'Name': Name,
                'Post':Post,
                'Post5': Post5,
                'Post20': Post20,
                'Post40': Post40,
                'Post60': Post60,
                'GTGDRong5days': GTGDRong5days,
                'GTGDRong20days': GTGDRong20days,
                'GTGDRong40days': GTGDRong40days,
                'GTGDRong60days': GTGDRong60days,
                'GTGDKLRong5days': GTGDKLRong5days,
                'GTGDKLRong20days': GTGDKLRong20days,
                'GTGDKLRong40days': GTGDKLRong40days,
                'GTGDKLRong60days': GTGDKLRong60days,
                'GTGDTTRong5days': GTGDTTRong5days,
                'GTGDTTRong20days': GTGDTTRong20days,
                'GTGDTTRong40days': GTGDTTRong40days,
                'GTGDTTRong60days': GTGDTTRong60days,
                'views': views,
               }

    return render(request,template,
                  context)


