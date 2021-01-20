from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.views.generic import View
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item,OrderItem,Order
from django.utils import timezone


class LoginView (View):
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None and user.is_active:
            login(request,user)
            messages.success(request,'Your Logged in!')
            return redirect ('home')
        messages.warning(request,'Username or Password is Incorrect!')
        return redirect ('login')  

    def get(self,request):
        return render(request,'practice/login.html')
    
def home(request):
    
    return render(request,'practice/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request,'Account created,Now Login!')
            return redirect('login')

    else:
        form= UserRegisterForm()
        messages.info(request,'Forms is Not Valid')
        return render(request,'practice/register.html',{'form': form}) 
        
     
def soap (request):
    context = {
        'products': Item.objects.filter(category ='SO')
    }
    return render(request,'practice/soap.html',context)

def shampo (request):
    return render(request,'practice/shampo.html')

def serum (request):
    return render(request,'practice/serum.html')

def facepack (request):
    return render(request,'practice/facepack.html')

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("orders")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("orders")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("orders")
def orders(request,slug):
    return render (request,'practice/order.html')

        

