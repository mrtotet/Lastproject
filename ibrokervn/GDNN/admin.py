from django.contrib import admin

# Register your models here.
from .models import GDNN, Viewed




class GDNNAdmin(admin.ModelAdmin):
    list_display = (
                            'pub_date',

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
                            'status',
                            )

    list_editable = ['status',]

    search_fields = ('pub_date','status',)
    list_filter = ('pub_date','status',)

    fieldsets = [
        ['Status', {'fields': ('status',)}],
        ['Tong GDNN', {'fields': ('Vol_Mua' ,'Vol_Ban' ,'Vol_Rong','Val_Mua' ,'Val_Ban' ,'Val_Rong',)}],
        ['KL tren san',{'fields': ('Vol_Mua_KL','Vol_Ban_KL','Val_Mua_KL', 'Val_Ban_KL','Val_KL_Rong',)}],
        ['KL TT', {'fields': ('Vol_Mua_TT','Vol_Ban_TT','Val_Mua_TT','Val_Ban_TT','Val_TT_Rong',)}],
        ['Ty le SH NN', {'fields': ('Room_NN_hientai','Total_Room_NN',
                            'Phantram_tong_SH_NN','SH_NN','Phantram_SH_NN',)}],
                ]

    list_per_page = 60
    save_on_top = True
    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='published')
        if rows_updated == 1:
            message_bit = "1 Ngày GD was"
        else:
            message_bit = "%s Ngày GDs were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)


    actions = [make_published]

admin.site.register(GDNN,GDNNAdmin)
admin.site.register(Viewed)