from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    def_address = models.CharField(max_length=500, default='')
    email = models.CharField(max_length=500)
    email_confirmation = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.user.username
        
class Code(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)