from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import Vimo, Viewed

class VimoAdmin(admin.ModelAdmin):
    list_display = ('publish','Tenthongtin','status','Anhhuong','Mucdo', 'CP_anhhuong','DangAH','AH','author')
    list_editable = ['Tenthongtin','status','Anhhuong','Mucdo', 'CP_anhhuong','DangAH','author']
    list_per_page = 15
    list_filter = ('publish','status','Anhhuong', 'DangAH')
    search_fields = ('Tenthongtin', 'publish','author')
    list_per_page = 60
    save_on_top = True

    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='published')
        if rows_updated == 1:
            message_bit = "1 TTVM was"
        else:
            message_bit = "%s TTVMs were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    actions = [make_published]


"""
    fieldsets = [
        ['Stock general information',{'fields': [('Symbol','Industry'),('author','S_status','publish')]}],
        ['Stock Fundemental Analyst', {
                                        'classes': ['collapse'],
                                        'fields': [ ('EnvironmentIndustry','W_Envi'),
                                            ('Management','W_Ma'),('Capital','W_Ca'), ('Qualify_asset','W_Qu_As'),
                                        ('Leverage', 'W_Lev'), ('Share', 'W_Share'), ('Perform', 'W_Perform')],
                                        }]
        ,]
    inlines = [
        StockInline,
    ]
"""

admin.site.register(Vimo,VimoAdmin)
admin.site.register(Viewed)

