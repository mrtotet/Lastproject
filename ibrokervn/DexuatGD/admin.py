
from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.

from django.contrib import admin



# Register your models here.
from .models import Stock_Detail, Recommend,Recommend_Category, Update_Trade, Estimate, NganhdandatTT
def published_selected_Objects(self, request, queryset):
    rows_updated = queryset.update(S_status='published')
    if rows_updated == 1:
        message_bit = "1 Row was"
    else:
        message_bit = "%s Rows were" % rows_updated
    self.message_user(request, "%s successfully marked as published." % message_bit)

class UpdateInline(admin.StackedInline):
    model = Recommend.Stock_chosen.through
    extra = 2

class EsitmateInline(admin.StackedInline):
    model = Estimate
    extra = 1

class NganhdandatTTInline(admin.TabularInline):
    model = NganhdandatTT
    extra = 1


class NganhdandatAdmin(admin.ModelAdmin):
    list_display = ('NgayRecommend','Nganh','Mucdo','CP_noibat',)

class StockAdmin(admin.ModelAdmin):
    list_display = ('Symbol','S_status','slug','San','Industry','SL_CP_Niem_yet','Ty_le_Freeloat','Ty_le_SHNN',)
    list_editable = ['S_status',]
    list_per_page = 15
    list_filter = ('Industry','S_status', 'publish','San',)
    search_fields = ('Symbol','San',)

    fieldsets = [
        ['Stock general information',{'fields': [('Symbol','San'),'Name','Industry',('S_status','publish')]}],
        ['Stock Basic Info', {
            'classes': ['collapse'],
            'fields': ['Website','So_dien_thoai','Dia_chi',
                       ('Quan', 'Tinh'),'Tong_Quan','SL_CP_Niem_yet', ('Ty_le_Freeloat','Ty_le_SHNN'),],
        }]
        ,]
    inlines = [
        EsitmateInline,
    ]
    actions = [published_selected_Objects]


from copy import deepcopy
from mezzanine.conf import settings
from mezzanine.core.admin import (DisplayableAdmin, OwnableAdmin,
                                  BaseTranslationModelAdmin)
from mezzanine.twitter.admin import TweetableAdminMixin

Recommend_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
Recommend_fieldsets[0][1]["fields"].insert(1, "categories")

Recommend_fieldsets = list(Recommend_fieldsets)
Recommend_fieldsets.insert(1, ("Nhận định TT", {
    "classes": ("collapse",),
    "fields": ("Streng","content","allow_comments")}))
Recommend_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories",)
class RecommendAdmin(TweetableAdminMixin, DisplayableAdmin, OwnableAdmin):
    list_display = ('title','publish_date','user','status','Streng','do_manh','list_of_stock','viewed',"admin_link")
    def list_of_stock(self, obj):
        return ("%s" % ','.join([name.title for name in obj.Stock_chosen.all()]))
    list_of_stock.short_description = 'list_stock_daily'
    list_filter = Recommend_list_filter
    #list_editable = ('status',)
    search_fields = ['title']
    fieldsets = Recommend_fieldsets
    filter_horizontal = ["categories",]
    actions = [published_selected_Objects]
    inlines = [
        NganhdandatTTInline,UpdateInline,
    ]
    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)

class RecommendCategoryAdmin(BaseTranslationModelAdmin):

    list_display = ('title',)
    def has_module_permission(self, request):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if "DexuatGD.Recommend_Category" in items:
                return True
        return False



class Update_Trade_Admin(admin.ModelAdmin):
    list_display = ('title','publish','Stock','DateRecommend','S_status','Trade','Indicator','Price_update',)
    actions = [published_selected_Objects]

class EsitmateAdmin(admin.ModelAdmin):
    list_display = ('title','Stock','publish','S_status','Postion','Style','Total_score','Gain_Loss','Risk','PE','PB',)
    list_editable = ('S_status','Postion','Style',)
    search_fields = ['title',]
    list_filter = ('S_status', 'Postion','Style',)
    fieldsets = [
        ['Stock general information',{'fields': ['title','Stock','publish','close_date',('author','S_status'),('Postion','Style'),'estimate_url','Risk','action']}],
        ['Stock Update Info', {
            'classes': ['collapse'],
            'fields': [('Price_open','Price_close'),('Price_change_5days','Price_change_20days','Price_change_60days'),('EPS','Bookvalue'),'Liquidity_30days'
                       ],
        }],
        ['Stock Fundemental Analyst', {
            'classes': ['collapse-closed'],
            'fields': [('EnvironmentIndustry', 'W_Envi'), ('Management', 'W_Ma'),
                       ('Qualify_asset', 'W_Qu_As'), ('Leverage', 'W_Lev'),
                       ('Top_industry', 'W_Top_industry'), ('Perform', 'W_Perform'),
                       ('Capital', 'W_Ca'), ('Liquidity', 'W_Li'),'Commnent' ],
        }]
        ,]
    inlines = [
        UpdateInline,
    ]
    actions = [published_selected_Objects]


admin.site.register(Recommend,RecommendAdmin)
admin.site.register(Stock_Detail,StockAdmin)
admin.site.register(Update_Trade,Update_Trade_Admin)
admin.site.register(Estimate,EsitmateAdmin)
admin.site.register(NganhdandatTT,NganhdandatAdmin)
admin.site.register(Recommend_Category,RecommendCategoryAdmin)