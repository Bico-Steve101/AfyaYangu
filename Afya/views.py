from allauth import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from Afya.forms import PaymentForm, MessageForm
from Afya.models import Product, Doctor, Cart, CartItem, Payment, Message
from django.http import JsonResponse


# Create your views here.
def index(request):
    doctors = Doctor.objects.all()
    product_count = Product.objects.count()
    doctor_count = Doctor.objects.count()
    user_count = User.objects.count()
    message_count = Message.objects.count()
    context = {
        'product_count': product_count,
        'doctor_count': doctor_count,
        'user_count': user_count,
        'message_count': message_count,
        'doctors': doctors,
    }
    return render(request, 'index.html', context)


def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    # Fetch and display messages sent to the specific doctor
    messages = Message.objects.filter(recipient=doctor.user)

    # Fetch information about all doctors
    all_doctors = Doctor.objects.all()

    is_doctor = hasattr(request.user, 'doctor')

    if request.method == 'POST':
        content = request.POST.get('content')
        sender = request.user
        Message.objects.create(sender=sender, recipient=doctor.user, content=content)
        return redirect('Afya:doctor_profile', doctor_id=doctor.id)

    context = {'doctor': doctor, 'messages': messages, 'is_doctor': is_doctor, 'all_doctors': all_doctors}
    return render(request, 'doctor_profile.html', context)

def reply_message(request, message_id):
    original_message = get_object_or_404(Message, id=message_id)

    # Ensure that the logged-in user is the intended recipient of the message and is a doctor
    if not (request.user == original_message.recipient and hasattr(request.user, 'doctor')):
        return HttpResponse("Unauthorized", status=401)

    if request.method == 'POST':
        content = request.POST.get('content')
        sender = request.user
        recipient = original_message.sender
        is_doctor_reply = hasattr(request.user, 'doctor')

        # Update the original message with the doctor's reply
        original_message.doctor_reply = content
        original_message.is_doctor_reply = is_doctor_reply
        original_message.save()

        # Redirect to the doctor's profile
        return redirect('Afya:doctor_profile', doctor_id=sender.doctor.id)

    if 'HTTP_X_REQUESTED_WITH' in request.headers and request.headers['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
        # If it's an AJAX request, return the reply form content as plain text
        reply_form_content = render(request, 'reply_form.html', {'reply_message': original_message})
        return HttpResponse(reply_form_content, content_type='text/html')

    is_doctor_reply = hasattr(request.user, 'doctor')
    context = {'original_message': original_message, 'is_doctor_reply': is_doctor_reply}
    return render(request, 'reply_message.html', context)


def pharmacy(request):
    products = Product.objects.all()
    return render(request, 'pharmacy.html', {'products': products})


@login_required(login_url='/login')
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required(login_url='/login')
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()

    messages.success(request, 'Item added to cart.')
    return redirect('Afya:pharmacy')


@login_required(login_url='/login')
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart_item = CartItem.objects.get(cart__user=request.user, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    messages.success(request, 'Item removed from cart.')
    return redirect('Afya:view_cart')


@login_required(login_url='/login')
def make_payment(request):
    cart = Cart.objects.get(user=request.user)
    form = PaymentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']

            # Check if a payment record already exists for the cart
            payment_record, created = Payment.objects.get_or_create(cart=cart)

            # Update the existing record or create a new one if it doesn't exist
            payment_record.phone_number = phone_number
            payment_record.save()

            # Your payment processing logic goes here
            # For simplicity, we'll just update the cart total price
            cart.total_price = sum(item.total_price() for item in cart.cartitem_set.all())
            cart.save()
            cart.cartitem_set.all()
            # Clear the cart after successful payment
            cart.cartitem_set.all().delete()

            messages.success(request, 'Payment successful. Your cart is cleared.')
            return redirect('Afya:view_cart')

    return render(request, 'make_payment.html', {'form': form})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('/')
        else:
            messages.error(request, 'Invalid login credentials.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required(login_url='/login')
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('/')


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('/')
        else:
            messages.error(request, 'Invalid registration details. Please try again.')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
