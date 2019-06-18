from __future__ import unicode_literals
from future.builtins import str
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from autoslug import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator

STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Stock_Detail(models.Model):
    publish =           models.DateTimeField(default=timezone.now, blank=True, null=True)
    S_created =         models.DateTimeField(auto_now_add=True,null=True)
    S_updated =         models.DateTimeField(auto_now=True,null=True)
    S_status =          models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='published',null=True)
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # The Dahl-specific manager.

    Symbol =            models.CharField("Mã CK",max_length=10, blank=True, null=True, unique = True)
    Name =              models.CharField("Tên Công Ty",max_length=50, blank=True, null=True)
    slug =              AutoSlugField(populate_from='Symbol',null=True)
    San =               models.CharField("Sàn",max_length=10, blank=True, null=True)
    Website =           models.CharField("Website",max_length=100, blank=True, null=True)
    So_dien_thoai =     models.CharField("Số điện thoại",max_length=50, blank=True, null=True)
    Dia_chi =           models.CharField("Địa chỉ",max_length=200, blank=True, null=True)
    Quan =              models.CharField("Quận/Huyện",max_length=50, blank=True, null=True)
    Tinh =              models.CharField("Tỉnh/Thành",max_length=100, blank=True, null=True)
    Tong_Quan =         models.TextField("Tổng quan",max_length=2000, blank=True, null=True)
    Industry =          models.CharField("Ngành",max_length=100, blank=True, null=True)
    SL_CP_Niem_yet =    models.BigIntegerField("Số lượng CP Niêm Yết", blank=True, null=True)
    Ty_le_Freeloat =    models.DecimalField("Free-loat", max_digits=4, decimal_places=2, blank=True, null=True)
    Ty_le_SHNN =        models.DecimalField("Tỷ lệ SH NN tối đa",max_digits=4, decimal_places=2, blank=True, null=True)

    viewed = models.IntegerField(default=0,blank=True, null=True)
    class Meta:
        ordering = ('Symbol',)
    def __str__(self):
        return self.Symbol
    def get_absolute_url(self):
        return reverse('nhandinhthitruong:phantichcophieu', args=[self.publish.year,
                                                 self.publish.strftime('%m'),
                                                 self.publish.strftime('%d'),
                                                 self.slug])

class Estimate (models.Model):
    POSITION_CHOICES = (  ('Mở vị thế', 'Mở vị thế'),
                        ('Đóng vị thế', 'Đóng vị thế')       )
    STYLE_CHOICES =             (   ('Dài hạn', 'Dài hạn'),
                                ('Ngắn hạn', 'Ngắn hạn'),
                             )
    title =             models.CharField(max_length=250, blank= True, null= True)
    Stock =             models.ForeignKey(Stock_Detail,related_name='estimate_Com',on_delete=models.CASCADE)
    #DateRecommend =     models.ForeignKey(Recommend, on_delete=models.CASCADE, blank= True , null= True)
    author =            models.ForeignKey(User, blank=True, null=True,related_name='author', on_delete=models.CASCADE)
    publish =           models.DateTimeField(default=timezone.now, blank=True, null=True)
    close_date =        models.DateTimeField(default=timezone.now, blank=True, null=True)
    S_created =         models.DateTimeField(auto_now_add=True,null=True)
    S_updated =         models.DateTimeField(auto_now=True,null=True)
    S_status =          models.CharField(max_length=10,
                                        choices=STATUS_CHOICES,
                                        default='draft',null=True)
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # The Dahl-specific manager.

    Postion=                models.CharField(max_length=20,
                                        choices=POSITION_CHOICES,
                                             blank=True,null=True)

    Style=                  models.CharField(max_length=10,
                                        choices=STYLE_CHOICES,
                                             blank=True,null=True)
    Price_open=             models.IntegerField("Giá mở vị thế",default=1,)
    Price_close=           models.IntegerField("Giá đóng vị thế",default=1,null=True, blank=True)

    @staticmethod
    def Cal_Gain_loss(a, b):
        Cal = round(((b-a)*100/a),2)
        if Cal >=0 :
            color = "green"
            change = "up"
        else:
            color = "red"
            change = "down"
        return Cal,color, change

    def Gain_Loss_close(self):
        return self.Cal_Gain_loss(self.Price_open, self.Price_close, )

    #@staticmethod
    #def Cal_PE_PB(a,b):
    #    Cal = (a/b)
    #    return  Cal

    #EPS =                   models.IntegerField("EPS",null=True, blank=True)
    #def PE(self):
    #    return self.Cal_PE_PB(self.Price_close, self.EPS)
    #Bookvalue =             models.IntegerField("Book Value",null=True, blank=True)
    #def PB(self):
    #    return self.Cal_PE_PB(self.Price_close, self.Bookvalue)
    Liquidity_30days =      models.BigIntegerField("KL GDTB 30 ngày",blank=True, null=True, )
    Price_change_5days=     models.IntegerField("Giá thay đổi 5 ngày",blank=True, null=True,)
    Price_change_20days=    models.IntegerField("Giá thay đổi 20 ngày",blank=True, null=True,)
    Price_change_60days=    models.IntegerField("Giá thay đổi 60 ngày",blank=True, null=True,)
    EnvironmentIndustry =   models.IntegerField(verbose_name="Môi trường kinh doanh",default=50, validators = [MaxValueValidator(100),MinValueValidator(0)],help_text='0-10')
    W_Envi =                models.PositiveIntegerField("Tỷ trọng",default=20, help_text='mặc định chuẩn, có thể thay đổi khi cần thiết')
    Management =            models.IntegerField("Quản trị Doanh Nghiệp",default=50,  validators = [MaxValueValidator(100),MinValueValidator(0)],help_text='0-10')
    W_Ma =                  models.IntegerField("Tỷ trọng",default=10, help_text='mặc định chuẩn, có thể thay đổi khi cần thiết')
    Qualify_asset =         models.IntegerField("Chất lượng tài sản",default=50,  validators = [MaxValueValidator(100),MinValueValidator(0)],help_text='0-10')
    W_Qu_As =               models.PositiveIntegerField("Tỷ trọng",default=10, help_text='mặc định chuẩn, có thể thay đổi khi cần thiết')
    Leverage =              models.IntegerField("Tỷ lệ vay nợ",default=50,  validators = [MaxValueValidator(100),MinValueValidator(0)],help_text='0-10')
    W_Lev =                 models.PositiveIntegerField("Tỷ trọng",default=10, help_text='mặc định chuẩn, có thể thay đổi khi cần thiết')
    Top_industry =          models.IntegerField("Khả năng gây ảnh hưởng trong ngành",default=50, validators = [MaxValueValidator(100),MinValueValidator(0)],help_text='0-10')
    W_Top_industry =        models.PositiveIntegerField("Tỷ trọng",default=10, help_text='mặc định chuẩn, có thể thay đổi khi cần thiết')
    Perform =               models.IntegerField("Hiệu suất kinh doanh",default=50,  validators = [MaxValueValidator(100),MinValueValidator(0)],help_text='0-10')
    W_Perform =             models.PositiveIntegerField("Tỷ trọng",default=15, help_text='mặc định chuẩn, có thể thay đổi khi cần thiết')
    Capital =               models.IntegerField("Vốn hóa",default=50,  validators = [MaxValueValidator(100),MinValueValidator(0)],help_text='0-10')
    W_Ca =                  models.IntegerField("Tỷ trọng",default=10,help_text='mặc định chuẩn, có thể thay đổi khi cần thiết')
    Liquidity =             models.IntegerField("Thanh khoản",default=50,  validators = [MaxValueValidator(100),MinValueValidator(0)],help_text='0-10')
    W_Li =                  models.IntegerField("Tỷ trọng",default=15, help_text='mặc định chuẩn, có thể thay đổi khi cần thiết')
    Commnent =              models.TextField("Đánh giá DN", max_length=2000, blank=True, null=True,help_text='mặc định chuẩn, có thể thay đổi khi cần thiết')
    #Indicator =             models.IntegerField(default=50,  validators = [MaxValueValidator(100),MinValueValidator(0)],help_text='0-100')
    action =                models.TextField('Nhận xét',max_length=2000, blank=True, null=True,help_text='Cho nhận xét về DN')
    Risk = models.IntegerField('Rủi ro',default=50, validators=[MaxValueValidator(100), MinValueValidator(0)],
                                    help_text='0-100')
    estimate_url =          models.URLField('URL',max_length= 500,blank=True, null=True,help_text='đường dẫn youtube hoặc url khác')

    @staticmethod
    def Calculatiion_score(a, b, c, d, e, f, g, h, i, j, k, l, m, n,o,p):
        full_Weight = (b + d + f + h + j + l + n +p)
        Cal_score = int(((a * b) + (c * d) + (e * f) + (g * h) + (i * j) + (k * l) + (m * n) + (o * p)) /full_Weight) #int cho dep so
        if Cal_score >=70 :
            domanh = "Rất tốt"
        elif Cal_score >=60 :
            domanh = "Tốt"
        elif Cal_score >=40 :
            domanh = "Trung bình"
        else:
            domanh = "Xấu"
        return  Cal_score,domanh

    def Total_score(self):
        return self.Calculatiion_score(self.EnvironmentIndustry, self.W_Envi,
                                       self.Management, self.W_Ma,
                                       self.Qualify_asset, self.W_Qu_As,
                                       self.Leverage, self.W_Lev,
                                       self.Top_industry, self.W_Top_industry,
                                       self.Perform, self.W_Perform,
                                       self.Capital, self.W_Ca,
                                       self.Liquidity, self.W_Li,
                                       )
    @staticmethod
    def risk1(a):
        So = int(a)
        if So >= 80:
            risk= "RẤT RỦI RO"
        elif So >= 60:
            risk= "RỦI RO"
        elif So >= 40:
            risk= "TRUNG TÍNH"
        elif So >= 30:
            risk = "AN TOÀN"

        else:
            risk = "RẤT AN TOÀN"
        return risk
    def RISK(self):
        return self.risk1(self.Risk)

    Title = AutoSlugField(populate_from='title', null=True)


    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title
    def get_verbose_name(self):
        return self._meta.verbose_name

from mezzanine.core.models import Displayable, Ownable, RichText, Slugged
from mezzanine.generic.fields import CommentsField, RatingField
from mezzanine.utils.models import AdminThumbMixin, upload_to
from mezzanine.conf import settings

class Recommend(Displayable, Ownable, RichText, AdminThumbMixin,):

    Stock_chosen =  models.ManyToManyField(Estimate, through= 'Update_Trade', verbose_name="Chọn CP", blank=True,related_name="Recommend")
    Streng =    models.IntegerField("Độ mạnh",null=True, blank=True, validators = [MaxValueValidator(100),MinValueValidator(0)], help_text='0-100')

    @staticmethod
    def sohoa(a):
        So = int(a)
        if So >= 80:
            Do_manh= "RẤT MẠNH"
        elif So >= 70:
            Do_manh = "MẠNH"
        elif So >= 60:
            Do_manh = "KHÁ MẠNH"
        elif So >= 40:
            Do_manh = "TRUNG BÌNH"
        elif So >= 30:
            Do_manh = "YẾU"

        else:
            Do_manh = "RẤT YẾU"
        return Do_manh
    def do_manh(self):
        return self.sohoa(self.Streng)
    categories = models.ManyToManyField("Recommend_Category",
                                        blank=True, related_name="Recommends")
    allow_comments = models.BooleanField(verbose_name="Allow comments",
                                         default=True)
    comments = CommentsField(verbose_name="Còn bạn nhận định thế nào về TT ?")
    rating = RatingField(verbose_name="Rating")
    related_posts = models.ManyToManyField("self",
                                 verbose_name=_("Related posts"), blank=True)
    viewed = models.IntegerField(default=0)
    def get_absolute_url(self):
        url_name = "nhandinhthitruong:daily"
        kwargs = {"slug": self.slug}
        date_parts = ("year", "month", "day")
        if settings.BLOG_URLS_DATE_FORMAT in date_parts:
            url_name = "nhandinhthitruong:daily_%s" % settings.BLOG_URLS_DATE_FORMAT
            for date_part in date_parts:
                date_value = str(getattr(self.publish_date, date_part))
                if len(date_value) == 1:
                    date_value = "0%s" % date_value
                kwargs[date_part] = date_value
                if date_part == settings.BLOG_URLS_DATE_FORMAT:
                    break
        return reverse(url_name, kwargs=kwargs)
    class Meta:
        verbose_name = "Recommend"
        verbose_name_plural = "Recommends"
        ordering = ('-publish_date',)
    def __str__(self):
        return self.title

class Recommend_Category(Slugged):
    class Meta:
        verbose_name = _("Recommend Category")
        verbose_name_plural = _("Recommend Categories")
        ordering = ("title",)
    @models.permalink
    def get_absolute_url(self):
        return ("nhandinhthitruong:NhandinhTT_DexuatGD_list_category", (), {"category": self.slug})

class NganhdandatTT (models.Model):
    NgayRecommend = models.ForeignKey(Recommend, on_delete=models.CASCADE,)
    Nganh = models.CharField("Ngành",max_length=200,)
    Mucdo = models.IntegerField("Độ mạnh",default=0,null=True, blank=True, validators = [MaxValueValidator(100),MinValueValidator(0)], help_text='0-100')
    CP_noibat = models.CharField(max_length=200)
    Mau_CHOICES =             (   ('red','Đỏ'),
                                ( 'yellow','Vàng',),
                                ('green','Xanh lá'),
                                ('blue','Xanh da trời'),
                                  )
    Mau = models.CharField("Màu",max_length=10,
                                        choices=Mau_CHOICES,
                                        blank= True,null=True)
    def __str__(self):
        return self. Nganh

class Update_Trade (models.Model):
    title =     models.CharField(max_length=250, blank= True, null= True)
    publish =           models.DateTimeField(default=timezone.now, blank=True, null=True)

    S_created =         models.DateTimeField(auto_now_add=True,null=True)
    S_updated =         models.DateTimeField(auto_now=True,null=True)
    S_status =          models.CharField(max_length=10,
                                        choices=STATUS_CHOICES,
                                        default='draft',null=True)
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # The Dahl-specific manager.
    Stock =       models.ForeignKey(Estimate,related_name='update_trade', on_delete=models.CASCADE)
    DateRecommend = models.ForeignKey(Recommend, on_delete=models.CASCADE, blank=True, null=True)
    GD_CHOICES =             (   ('Mua mới', 'Mua mới'),
                                ('Mua thêm', 'Mua thêm'),
                                ('Nắm  giữ', 'Nắm  giữ'),
                                ('Chốt lời', 'Chốt lời'),
                                ('Cắt lỗ', 'Cắt lỗ'),
                                ('Bán bớt', 'Bán bớt'),
                                ('Bán hết', 'Bán hết')     )
    Trade=                  models.CharField(max_length=10,
                                        choices=GD_CHOICES,
                                             blank=True,null=True)

    @staticmethod
    def color_trade(a):
        if a == 'Mua mới':
            color = "green"
        elif a == 'Mua thêm':
            color = "lime"
        elif a == 'Nắm  giữ':
            color = "yellow"
        elif a == 'Chốt lời':
            color = "blue"
        elif a == 'Cắt lỗ':
            color = "red"
        elif a == 'Bán bớt':
            color = "gold"
        else:
            color = "violet"
        return color
    def Color_Trade(self):
        return self.color_trade(self.Trade)
    Price_update=           models.IntegerField("Giá cập nhật",default=1,)
    Indicator =             models.IntegerField(default=50,  validators = [MaxValueValidator(100),MinValueValidator(0)])
    action =                models.TextField("Đề xuất GD", max_length=2000, blank=True, null=True)
    @staticmethod
    def sohoa(a):
        So = int(a)
        if So >= 80:
            Do_manh= "RẤT MẠNH"
        elif So >= 70:
            Do_manh = "MẠNH"
        elif So >= 60:
            Do_manh = "KHÁ MẠNH"
        elif So >= 40:
            Do_manh = "TRUNG BÌNH"
        elif So >= 30:
            Do_manh = "YẾU"

        else:
            Do_manh = "RẤT YẾU"
        return Do_manh
    def do_manh(self):
        return self.sohoa(self.Indicator)



    class Meta:
        ordering = ('publish',)

class view_tonghopTT(models.Model):
    view_tonghop =    models.BigIntegerField("lượt xem trang TH", blank=True,default=0, null=True)

