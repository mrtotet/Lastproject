from __future__ import unicode_literals
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils import timezone


from mezzanine import template

User = get_user_model()

register = template.Library()

from django.shortcuts import render, redirect, get_object_or_404

from Vimo.models import Vimo

@register.inclusion_tag('vimosimple.html')
def Vimosimple():

    ConAH = Vimo.objects.filter(DangAH=1).order_by('-Mucdo')
    return {'ConAH': ConAH, }


from django.db.models import Sum

from GDNN.models import GDNN, Viewed
# Create your views here.
@register.inclusion_tag('TKgdnn.html')
def TKgdnn():
    Name = [f for f in GDNN._meta.get_fields() if f.name != 'id' if f.name != 'status']
    Post = GDNN.objects.filter(status='published')
    Post5 = Post.order_by('id')[:5]
    Post20 = Post.order_by('id')[:20]
    Post40 = Post.order_by('id')[:40]
    Post60 = Post.order_by('id')[0:60]
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
               }

    return context


from DexuatGD.models import Recommend, Recommend_Category

@register.simple_tag
def Nhandinh_detail_moinhat():
    Nhandinh_posts = Recommend.objects.published()
    Post_moinhat_1 = Nhandinh_posts.latest('publish_date')
    return Post_moinhat_1

#@register.simple_tag
#def linkrecommendmoinhat():
#    Nhandinh_posts = Recommend.objects.published()
#    Post_moinhat_1 = Nhandinh_posts.latest('publish_date')
#    return Post_moinhat_1

@register.as_tag
def Nhandinh_months(*args):
    """
    Put a list of dates for blog posts into the template context.
    """
    dates = Recommend.objects.published().values_list("publish_date", flat=True)
    tz = timezone.get_current_timezone()
    dates = [d.astimezone(tz) for d in dates]
    date_dicts = [{"date": datetime(d.year, d.month, 1)} for d in dates]
    month_dicts = []
    for date_dict in date_dicts:
        if date_dict not in month_dicts:
            month_dicts.append(date_dict)
    for date_dict in month_dicts:
        date_dict["Nhandinh_count"] = date_dicts.count(date_dict)
    return month_dicts


@register.as_tag
def Nhanhdinh_categories(*args):
    """
    Put a list of categories for blog posts into the template context.
    """
    posts = Recommend.objects.published()
    categories = Recommend_Category.objects.filter(Recommends__in=posts)
    return list(categories.annotate(post_count=Count("Recommends")))

@register.as_tag
def nhandinh_authors(*args):
    """
    Put a list of authors (users) for blog posts into the template context.
    """
    blog_posts = Recommend.objects.published()
    authors = User.objects.filter(recommends__in=blog_posts)
    return list(authors.annotate(post_count=Count("blogposts")))




