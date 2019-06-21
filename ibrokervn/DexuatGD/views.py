from __future__ import unicode_literals
from future.builtins import str, int
from calendar import month_name
from django.contrib.auth import get_user_model
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import paginate

User = get_user_model()

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django import forms

import django_excel as excel
from .models import Stock_Detail, Recommend, Recommend_Category, NganhdandatTT, Estimate
from django.contrib.admin.views.decorators import staff_member_required

data =[1, 2, 3]
class UploadFileForm(forms.Form):
    file = forms.FileField()

@staff_member_required
def import_Stock_basic_info(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            request.FILES['file'].save_to_database(
                name_columns_by_row=0,
                model=Stock_Detail,
                mapdict=[   'Symbol',
                            'Name',
                            'San',
                            'Website',
                            'So_dien_thoai',
                            'Dia_chi',
                            'Quan',
                            'Tinh',
                            'Tong_Quan',
                            'Industry',
                            'SL_CP_Niem_yet',
                            'Ty_le_Freeloat',
                            'Ty_le_SHNN',
                            ]
            )
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    template = "pages/toidautu/nhandinhthitruong/import_Doanhnghiep.html"
    context = {'form': form}
    return render(
        request,
        template,
        context)

def Nhandinh_list(request,tag=None, year=None, month=None, username=None,
                   category=None, template="pages/toidautu/NhandinhTT_DexuatGD_list.html",
                   extra_context=None,category_slug=None):
    Nhandinh_posts = Recommend.objects.published(for_user=request.user)
    Post_moinhat_60 = Nhandinh_posts.order_by('-publish_date')[:60]
    templates = []
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        Nhandinh_posts = Nhandinh_posts.filter(keywords__keyword=tag)
    if year is not None:
        Nhandinh_posts = Nhandinh_posts.filter(publish_date__year=year)
        if month is not None:
            Nhandinh_posts = Nhandinh_posts.filter(publish_date__month=month)
            try:
                month = _(month_name[int(month)])
            except IndexError:
                raise Http404()
    if category is not None:
        category = get_object_or_404(Recommend_Category, slug=category)
        Nhandinh_posts = Nhandinh_posts.filter(categories=category)
        templates.append(u"pages/toidautu/NhandinhTT_DexuatGD_list_%s.html" %
                          str(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        Nhandinh_posts = Nhandinh_posts.filter(user=author)
        templates.append(u"pages/toidautu/NhandinhTT_DexuatGD_list_%s.html" % username)
    prefetch = ("categories", "keywords__keyword")
    Nhandinh_posts = Nhandinh_posts.select_related("user").prefetch_related(*prefetch)
    Nhandinh_posts = paginate(Nhandinh_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"Nhandinh_posts": Nhandinh_posts,"Post_moinhat_60": Post_moinhat_60,"year": year, "month": month,
               "tag": tag, "category": category,"author": author}
    context.update(extra_context or {})
    templates.append(template)
    return TemplateResponse(request, templates, context)

def Nhandinh_detail_moinhat(request, year=None, month=None, day=None,
                   template="pages/toidautu/NhandinhTT_DexuatGD.html",
                   extra_context=None):
    Nhandinh_posts = Recommend.objects.published(for_user=request.user)
    Post_moinhat_1 = Nhandinh_posts.latest('publish_date')
    Post_moinhat_1.viewed +=1
    Post_moinhat_1.save()
    related_posts = Post_moinhat_1.related_posts.published(for_user=request.user)
    context = {"Post_moinhat_1": Post_moinhat_1,"Nhandinh_posts": Nhandinh_posts,
                "related_posts": related_posts}
    context.update(extra_context or {})
    templates = [u"pages/toidautu/NhandinhTT_DexuatGD_moinhat.html", template]
    return TemplateResponse(request, templates, context)

def Nhandinh_detail(request, slug, year=None, month=None, day=None,
                   template="pages/toidautu/NhandinhTT_DexuatGD.html",
                   extra_context=None):
    Nhandinh_posts_all = Recommend.objects.published(for_user=request.user)
    Post_moinhat_40 = Nhandinh_posts_all.order_by('-publish_date')[:40]
    #Post_moinhat_40 = reversed(Post_moinhat_40) # đảo ngược đồ thị từ cũ tới mới
    Post_moinhat_40_ruiro = Nhandinh_posts_all.order_by('-publish_date')[:40]
    Nhandinh_posts = get_object_or_404(Nhandinh_posts_all, slug=slug)
    Nhandinh_posts.viewed +=1
    Nhandinh_posts.save()
    related_posts = Nhandinh_posts.related_posts.published(for_user=request.user)
    context = {"Post_moinhat_40_ruiro": Post_moinhat_40_ruiro,"Nhandinh_posts_all": Nhandinh_posts_all,"Post_moinhat_40": Post_moinhat_40,"Nhandinh_posts": Nhandinh_posts,"editable_obj": Nhandinh_posts,
                "related_posts": related_posts}
    context.update(extra_context or {})
    templates = [u"pages/toidautu/NhandinhTT_DexuatGD_%s.html" % str(slug), template]
    return TemplateResponse(request, templates, context)

from .models import view_tonghopTT
def Tonghopthongtin(request):
    context ={}
    templates = 'pages/toidautu/tonghopthongtin.html'
    views = get_object_or_404(view_tonghopTT)
    views.view_tonghop +=1
    views.save()
    context = {'views':views,}
    return render(request, templates,context)


@login_required
def stock_detail(request, year, month, day, post):
    post = get_object_or_404(Stock_Detail, slug=post,
                                   S_status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    post.viewed +=1
    post.save()
    estimate = post.estimate_Com.all()
    estimate_close = estimate.filter(Postion = 'Đóng vị thế')
    estimate_moinhat = estimate.latest("publish")
    Update_trade_all = estimate_moinhat.update_trade.all()
    Update_trade_latest = estimate_moinhat.update_trade.latest("publish")
    recommend = estimate_moinhat.Recommend

    def Cal_Gain_loss(a, b):
        Cal = round(((b - a) * 100 / a), 2)
        if Cal >=0 :
            color = "green"
            change = "up"
        else:
            color = "red"
            change = "down"
        return Cal,color, change

    Gain_Loss_update =Cal_Gain_loss(estimate_moinhat.Price_open, Update_trade_latest.Price_update)

    def Cal_PE_PB(a,b):
        Cal = (a/b)
        return  Cal

    PE_open = Cal_PE_PB(estimate_moinhat.Price_open,estimate_moinhat.EPS)
    PB_open = Cal_PE_PB(estimate_moinhat.Price_open,estimate_moinhat.Bookvalue)
    PE_update = Cal_PE_PB(Update_trade_latest.Price_update,estimate_moinhat.EPS)
    PB_update = Cal_PE_PB(Update_trade_latest.Price_update,estimate_moinhat.Bookvalue)


    context = {"post":post,
               "estimate" : estimate,
               "estimate_close" : estimate_close ,
               "recommend": recommend,
               "Gain_Loss_update": Gain_Loss_update,
               "PE_open": PE_open,
               "PB_open": PB_open,
               "PE_update": PE_update,
               "PB_update": PB_update,
               "Update_trade_all":Update_trade_all,
               "Update_trade_latest": Update_trade_latest,
               "estimate_moinhat" : estimate_moinhat}

    templates = 'pages/toidautu/phantichcophieu.html'
    return render(request, templates,context)

