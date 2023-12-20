from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from Afya import views


app_name = 'Afya'

urlpatterns = [
                  path('', views.index, name="index"),
                  path('login/', views.user_login, name='login'),
                  path('register/', views.user_register, name='register'),
                  path('logout/', views.user_logout, name='logout'),
                  path('about/', views.about, name="about"),
                  path('contact/', views.contact, name="contact"),
                  path('cart/', views.view_cart, name='view_cart'),
                  path('phamarcy/', views.pharmacy, name="pharmacy"),
                  path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
                  path('make_payment/', views.make_payment, name='make_payment'),
                  path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

                  path('doctor_profile/<int:doctor_id>/', views.doctor_profile, name='doctor_profile'),
                  path('reply_message/<int:message_id>/', views.reply_message, name='reply_message'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
