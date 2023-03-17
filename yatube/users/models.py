from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()


    def __str__(self) -> str:
        return self.user.username
        
