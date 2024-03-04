from django.contrib import admin
from auction.models import User, Category, Listing, Comment, Bid, Brand

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Brand)