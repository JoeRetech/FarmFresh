from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests
from .models import Product,Cart,Billing,FarmerRequest
from django.contrib.auth.decorators import login_required,user_passes_test

from .forms import EmailForm
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordResetForm


# Create your views here.
def index(request):
    return render(request,'index.html')



def admin(request):
    return redirect('/admin/')

def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(email = email)
        
        if user.exists():
            messages.info(request, "Email already taken")
            return redirect('/signup/')
        
        user =User.objects.create(
            username = email,
            email = email,
            password = password
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Account created Successfully")
        return redirect('/login_page/')
    return render(request, 'signup.html')
        
    

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
       
        
        if not User.objects.filter(username=email).exists():
            messages.info(request, "Invalid Username")
            return redirect('/login_page/')
        
        user = authenticate(username = email,password = password )
        print(user)
        
        if user is None:
            messages.info(request, "Invalid Password")
            return redirect('/login_page/')
        
        else:
            login(request,user)
            return redirect('/product/')
    
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/')



@login_required(login_url="/login_page/")
def products(request):
    all_products = Product.objects.all()
    context = {
        'products': all_products
    }
    return render(request, 'product.html', context)

def category_products(request, category):
    category_products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'category_products': category_products
    }
    return render(request, 'product.html', context)

@login_required(login_url='/login/')
def update_cart(request,id):
    product = Product.objects.get(id=id)
    if(Cart.objects.filter(username = request.user, product=product).exists()):
        old_quantity = Cart.objects.values_list('quantity', flat=True).get(username=request.user, product=product)
        if(request.GET.get('name') == 'increase_cart'):
            updated_quantity = old_quantity + 1
            Cart.objects.filter(username = request.user, product=product).update(quantity = updated_quantity)
        elif(request.GET.get('name') == 'decrease_cart'):
            updated_quantity = old_quantity - 1
            Cart.objects.filter(username = request.user, product=product).update(quantity = updated_quantity)
        elif(request.GET.get('name') == 'delete_cart_item'):
            item_to_delete = Cart.objects.get(username=request.user, product=product)
            item_to_delete.delete()
    else:
        cart_item = Cart(username = request.user, product=product)
        cart_item.save()
    return redirect('/cart/')

@login_required(login_url='/login/')
def cart(request):
    cartitems = Cart.objects.filter(username=request.user)
    total_amount = 0
    if(cartitems):
        for item in cartitems:
            sub_total = item.product.price * item.quantity
            total_amount += sub_total
    return render(request, 'addtocart.html', {'cartitems':cartitems, 'total_amount':total_amount})
def checkout(request):
    total=request.GET.get('total')
    if request.method == 'POST':
        userName =request.POST.get('userName')
        firstName =request.POST.get('firstName')
        lastName =request.POST.get('lastName')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        pin = request.POST.get('pin')
        total = request.POST.get('total')
        payment_method=request.POST.get('paymentMethod')
        Billing.objects.create(userName=userName,firstName=firstName,lastName=lastName,address=address,country=country,state=state,pin=pin,payment_method=payment_method,amount=total)
        Cart.objects.all().delete()
        return render(request,'success.html')
    return render(request,'checkout.html',{'total':total})

def farmerrequest(request):
    if request.method == 'POST':
        name = request.POST.get('name')    
        email = request.POST.get('email')    
        address= request.POST.get('address')
        reqmsg= request.POST.get('reqmsg')

        FarmerRequest.objects.create(name=name,email=email,address=address,reqmsg=reqmsg)
        messages.info(request, "Request Sended Successfully")
    return render(request,'farmerRequest.html')    


def adminreq(request):
    requests=FarmerRequest.objects.all()
    return render(request,'requests.html',{'requests':requests})


def admin_check(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(admin_check, login_url='/login/')
def send_email(request):
    form = EmailForm()
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            requester = form.cleaned_data['requester']
            message = form.cleaned_data['message']

            subject = 'Message from the FarmFresh'
            from_email = 'amlananshu6a@gmail.com'
            recipient_list = [requester.email]

            send_mail(subject, message, from_email, recipient_list)

            return redirect('index')  # Redirect to a thank-you page or any other desired page

    return render(request, 'send_email.html', {'form': form})


 
        
         