from django.contrib import admin

# Register your models here.

from .models import ProductCategory, Product, DoctorCategory, Doctor, Advert, Cart, CartItem, Message

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(DoctorCategory)
admin.site.register(Doctor)
admin.site.register(Advert)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Message)