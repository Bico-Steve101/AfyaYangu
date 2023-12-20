from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/product', default='media/adverts/background.jpg')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.product.price * self.quantity


class Payment(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class DoctorCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey(DoctorCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/Doctor', default='media/Doctor/female-doctor.jpg',
                              validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('doctor_profile', kwargs={'doctor_id': self.id})

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_doctor_reply = models.BooleanField(default=False)
    doctor_reply = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"From {self.sender} to {self.recipient} on {self.timestamp}"


class Advert(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='media/adverts', default='media/adverts/background.jpg')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title
