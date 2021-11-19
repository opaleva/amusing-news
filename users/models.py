from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    city = models.CharField(max_length=15)
