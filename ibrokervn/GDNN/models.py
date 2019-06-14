from django.db import models

class GDNN(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    pub_date = models.DateField("Ngày", blank=True, null=True)

    Vol_Mua = models.BigIntegerField("KL Mua",default=0, blank=True, null=True)
    Val_Mua = models.BigIntegerField("GT Mua",default=0, blank=True, null=True)
    Vol_Ban = models.BigIntegerField("KL Bán",default=0, blank=True, null=True)
    Val_Ban = models.BigIntegerField("GT Bán",default=0, blank=True, null=True)
    Vol_Rong = models.BigIntegerField("KLGD Ròng",default=0, blank=True, null=True)

    Val_Rong = models.BigIntegerField("GTGD Ròng",default=0, blank=True, null=True)

    Vol_Mua_KL = models.BigIntegerField("KL Mua Khớp Lệnh",default=0, blank=True, null=True)
    Val_Mua_KL = models.BigIntegerField("GT Mua Khớp Lệnh",default=0, blank=True, null=True)
    Vol_Ban_KL = models.BigIntegerField("KL Bán Khớp Lệnh",default=0, blank=True, null=True)
    Val_Ban_KL = models.BigIntegerField("GT Bán Khớp Lệnh",default=0, blank=True, null=True)

    Val_KL_Rong = models.BigIntegerField("GTGD Khớp Lệnh Ròng",default=0, blank=True, null=True)

    Vol_Mua_TT = models.BigIntegerField("KL Mua TT",default=0, blank=True, null=True)
    Val_Mua_TT = models.BigIntegerField("GT Mua TT",default=0, blank=True, null=True)
    Vol_Ban_TT = models.BigIntegerField("KL Bán TT",default=0, blank=True, null=True)
    Val_Ban_TT = models.BigIntegerField("GT Bán TT",default=0, blank=True, null=True)

    Val_TT_Rong = models.BigIntegerField("GTGD TT Ròng",default=0, blank=True, null=True)

    Room_NN_hientai = models.BigIntegerField("Room NN hiện tại",default=0, blank=True, null=True)
    Total_Room_NN = models.BigIntegerField("Tổng Room NN",default=0, blank=True, null=True)
    Phantram_tong_SH_NN = models.DecimalField("Tổng phần trăm room NN",max_digits=4, decimal_places=2, blank=True, null=True)
    SH_NN = models.BigIntegerField("Tổng SH NN",default=0, blank=True, null=True)
    Phantram_SH_NN = models.DecimalField("Tổng phần trăm SH NN",max_digits=4, decimal_places=2, blank=True, null=True)




    class Meta:
        ordering = ('-pub_date',)


# Theo doi viewed tren cac trang
class Viewed(models.Model):
    viewed_gdnn = models.BigIntegerField(default=0)