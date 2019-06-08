from django.db import models
#from phonenumber_field.modelfields import PhoneNumberField
class MyProfile(models.Model):
    user = models.OneToOneField("auth.User",related_name="clientprofile")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name = "Ngày sinh")
    phone = models.CharField(null=True, blank=True, verbose_name = "Số Điện thoại", max_length=12)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True, verbose_name = "Ảnh đại diện",)
    contact_address = models.CharField(null=True, blank=True, verbose_name = "Địa chỉ liên lạc", max_length=150)

