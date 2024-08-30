from django.db import models

class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number
