from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from .managers import UserManager
class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=20)
    is_active = models.BooleanField(default=True)
    level_access = models.PositiveIntegerField(default=0, choices=[(0, 'Seller'), (1, 'SubSeller'), (10, 'Admin')])

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["is_active", "level_access"]  # fields that will show in createsuperuser

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.level_access == 10:
            return True
        return False
