from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator




class Vimo(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    author = models.ForeignKey(User,
                               related_name='Vimo', on_delete=models.CASCADE)
    publish = models.DateField(default=date.today)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    #published = PublishedManager()

    Tenthongtin = models.CharField(max_length=200)
    AH_CHOICES = (
        (0, 'Xấu'),
        (1, 'Tốt'),
        (2, 'Chưa XĐ')
    )
    Anhhuong = models.IntegerField(default=2,
                                   choices=AH_CHOICES
                                   # validators=[MaxValueValidator(1),MinValueValidator(0)]
                                   )
    Nhanxet = models.TextField("Nhận xét", max_length=2000, blank=True, null=True)

    @staticmethod
    def sohoa(a):
        So = int(a)
        if So == 0:
            color = "red"
        elif So == 1:
            color = "green"
        else:
            color = "yellow"
        return color

    def AH(self):
        return self.sohoa(self.Anhhuong)

    @staticmethod
    def sohoa1(a):
        So = int(a)
        if So == 0:
            anhhuong = "Tiêu cực"
        elif So == 1:
            anhhuong = "Tích cực"
        else:
            anhhuong = "Chưa rõ ràng"
        return anhhuong

    def anh_huong(self):
        return self.sohoa1(self.Anhhuong)

    Mucdo = models.IntegerField(default=0,
                                validators=[MaxValueValidator(100),
                                            MinValueValidator(0)])



    CP_anhhuong = models.CharField(max_length=200)
    ConAH_CHOICES = (
        (0, 'Hết AH'),
        (1, 'Còn AH'),
    )
    DangAH = models.IntegerField(default=1,
                                 choices=ConAH_CHOICES
                                 # validators=[MaxValueValidator(1),MinValueValidator(0)]
                                 )

    @staticmethod
    def sohoa3(a):
        So = int(a)
        return So

    def dang_AH(self):
        return self.sohoa3(self.DangAH)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.Tenthongtin

    @staticmethod
    def sohoa4(a):
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
        return self.sohoa4(self.Mucdo)


# Theo doi viewed tren cac trang
class Viewed(models.Model):
    viewed_list_Vimo = models.BigIntegerField(default=0)


