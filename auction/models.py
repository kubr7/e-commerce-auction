from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from datetime import date
from django.core.validators import RegexValidator


class User(AbstractUser):
    default_auto_field = 'django.db.models.BigAutoField'
    name = models.CharField(default='', max_length=20)
    firstName = models.CharField(default='', max_length=20)
    lastName = models.CharField(default='', max_length=20)
    dob = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    dob = models.DateField(default=date.today)
    mobileNo = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(regex=r'^\d{10}$', message='Enter a valid 10-digit mobile number.')
        ],
        help_text='Enter your 10-digit mobile number',
        null=True,
        blank=True
    )
    address = models.CharField(max_length=255, help_text='Enter your address', null=True, blank=True) 

    def full_name(self):
        return f"{self.firstName} {self.lastName}"
    
    def __str__(self):
        return self.username

class Brand(models.Model):
    default_auto_field = 'django.db.models.BigAutoField'
    brandName = models.CharField(max_length=50)

    def __str__(self):
        return self.brandName

class Category(models.Model):
    default_auto_field = 'django.db.models.BigAutoField'
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName

class Bid(models.Model):
    default_auto_field = 'django.db.models.BigAutoField'
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")

class Listing(models.Model):
    default_auto_field = 'django.db.models.BigAutoField'
    name = models.CharField(max_length=50)
    imageurl = models.CharField(max_length=1000)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True, related_name="brand")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    description = models.CharField(max_length=1000)
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    watchlist = models.ManyToManyField(User, blank=True, related_name="listingWatchList")
    isExpired = models.BooleanField(default=False)
    end_time = models.DateTimeField(default=timezone.now() + timedelta(days=1))
    # end_time = models.DateTimeField(default=datetime(2023, 12, 31, 23, 59, 59))

    def __str__(self):
        return self.name

class Comment(models.Model):
    default_auto_field = 'django.db.models.BigAutoField'
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="listingComment")
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"