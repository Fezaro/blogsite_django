from django.db import models
from django.conf import settings


class Profile(models.Model):
    """Profile model extends the user profile """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #
    role = models.CharField(max_length=20, default='Social Observer')
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        """string representation of model object"""
        return f'Profile for user {self.user.username}'
    
