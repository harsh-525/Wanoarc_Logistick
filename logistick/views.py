from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from logistick.models import Fquestion, Stock, OrderDetail, Order


def home_page(request):

    return render(request, 'home.html')

def validateUser(request):
    if request.user.is_authenticated:
        return True
    else:
        return False

def get_orders_customer(request):
    orders = Order.objects.filter(c_id=request.user.id)
    #print(orders)
    data=[]
    for order in orders:
        data.append(OrderDetail.objects.filter(order_id=order.id))

    return data

def corders(request):

    context = {'orders': get_orders_customer(request)}
    return render(request, 'customers_orders.html', context)

def placestock(request):

    if validateUser(request):
        stockid = request.POST.get('stockid')
        stocks = Stock.objects.filter(id=stockid).first()
        #print(stocks)
        context = {"stock": stocks }
        return render(request, 'customer_placestock.html',context)
    return render(request, 'customer_login.html')
def get_all_stocks():
    stocks = Stock.objects.all()
    print(stocks)
    return stocks

def get_filter_stocks(string):
    stocks = Stock.objects.filter( Q(by__contains=string)
                                   | Q(name__contains=string)
                                   | Q(description__contains=string))
    print(stocks)
    return stocks

def corders_search(request):
    word = (request.GET.get("search"))
    if validateUser(request):
        orders = get_orders_customer(request)
        print(orders)
        context = {'stocks': get_filter_stocks(word)}
        return render(request, 'customer_home.html', context)
    return render(request, 'customer_login.html')

def clogin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Fquestion.objects.filter(username=username)
        if not user.exists():
            #messages.warning(request, 'Account not found ')
            messages.warning(request,"Invalid Username")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif user[0].is_vendor:
            messages.warning(request, "Invalid Customer")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(f"{username} == {user[0].username}")
            print(f"{password} == {user[0].password}")
            user = authenticate(username = username, password = password)
            if not user:
                messages.warning(request,"Error: Invalid password")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                print("user login:"+user.username)
                login(request, user)
                context = {'stocks': get_all_stocks()}#get_all_stocks()}
                return render(request, 'customer_home.html', context)
    else:
        if validateUser(request):
            orders=get_orders_customer(request)
            print(orders)
            context = {'stocks': get_all_stocks()}
            return render(request, 'customer_home.html', context)
        return render(request, 'customer_login.html')

def get_v_stocks(id):
    stocks = Stock.objects.filter(v_id=id)
    print(stocks)
    return stocks


def viewstock(request):
    messages.info(request,"Refresh")
    context = {'stocks': get_v_stocks(request.user.id)}
    return render(request, 'vendor_home.html', context)

def sadd(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        company = request.POST.get('company')
        price = request.POST.get('price')
        user = Fquestion.objects.filter(id = request.user.id)
        newStock = Stock.objects.create(v_id=user[0], name=name,quantity=quantity,price=price,description="None", by=company)
        newStock.save()
        context = {'stocks': get_v_stocks(request.user.id)}
        messages.warning(request, "Saved")
        # todo messages are not working
        return render(request, 'vendor_home.html', context)
    else:
        context = {'stocks': get_v_stocks(request.user.id)}
        messages.warning(request, "Saved")
        # todo messages are not working
        return render(request, 'vendor_home.html', context)
def supdate(request):

    if request.method == 'PUT':
        id = request.POST.get('id')
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        stock = Stock.objects.filter(id=id)[0]
        stock.name = name
        stock.quantity = quantity
        stock.price = price
        stock.save()

        #print(stock)
        context = {'stocks': get_v_stocks(request.user.id)}
        messages.warning(request, "Saved")
        #todo messages are not working
        return render(request, 'vendor_home.html', context)
    elif request.method == 'POST':
        id = request.POST.get('id')
        print(id)
        stock = Stock.objects.filter(id=id)[0]
        stock.delete()
        context = {'stocks': get_v_stocks(request.user.id)}
        messages.warning(request, "Deleted")
        # todo messages are not working
        return render(request, 'vendor_home.html', context)
def vlogin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Fquestion.objects.filter(username=username)

        if not user.exists():
            #messages.warning(request, 'Account not found ')
            messages.warning(request,"Username is invalid")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif not user[0].is_vendor:
            messages.warning(request,"Invalid Vendor")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            user = authenticate(username = username, password = password)
            if not user:
                messages.warning(request,"Invalid password")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                print("user login:"+user.username)
                login(request, user)
                stocks = get_v_stocks(user.id)
                context = {'stocks': stocks}
                return render(request, 'vendor_home.html',context)
    else:
        if validateUser(request):
            stocks = get_v_stocks(request.user.id)
            print(request.user.id)
            context = {'stocks': stocks}
            return render(request, 'vendor_home.html', context)
        return render(request, 'vendor_login.html')

def logout_handler(request):
    logout(request)
    return redirect('/')


def forgot(request):
    #
    if request.method == 'POST':
        email = request.POST.get('email')
        #print(email)
        user = Fquestion.objects.filter(email=email)

        if not user.exists():
            messages.warning(request, "Error: Invalid email address")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            #print(user[0].email)
            context = {'new': user[0]}
            return render(request, "forgotpass_step_two.html", context)
    else:

        return render(request, "forgotpass.html")

def forgot2(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        answer_one = request.POST.get('answer_one')
        answer_two = request.POST.get('answer_two')
        # print(email)

        user = Fquestion.objects.filter(email=email)[0]
        context = {'new': user}
        if answer_one != user.answer_one:
            messages.warning(request,"Invalid submission for answer one")
            return render(request, "forgotpass_step_two.html", context)
        elif answer_two != user.answer_two:
            messages.warning(request,"Invalid submission for answer two")
            return render(request, "forgotpass_step_two.html", context)
        else:
            return render(request, "forgotpass_step_three.html", context)
    else:
        return render(request, "forgotpass.html")

def forgot3(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        # print(email)

        user = Fquestion.objects.filter(email=email)[0]
        context = {'new': user}
        if password != re_password:
            messages.warning(request,"Invalid submission password mismatch")
            return render(request, "forgotpass_step_three.html", context)
        else:
            try:
                user.set_password(password)
                user.save()
                return render(request, "home.html")
            except Exception as error:
                messages.warning(request,error)
                return render(request, "forgotpass_step_three.html", context)

    else:
        return render(request, "forgotpass.html")
def validateEmail(email):
    data = Fquestion.objects.filter(email = email)
    if data:
        raise Exception("UNIQUE constraint: Email already exists")

def cregister(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        question_one = request.POST.get('question_one')
        answer_one = request.POST.get('answer_one')
        question_two = request.POST.get('question_two')
        answer_two = request.POST.get('answer_two')
        customer = False
        flag = register_User(request,first_name,last_name,email,username,password,question_one,answer_one,question_two,answer_two,customer)

        if flag:
            return render(request, "customer_login.html")
        else:
            return render(request, "customer_register.html")
    else:
        return render(request, "customer_register.html")

def vregister(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        question_one = request.POST.get('question_one')
        answer_one = request.POST.get('answer_one')
        question_two = request.POST.get('question_two')
        answer_two = request.POST.get('answer_two')
        customer = True
        flag = register_User(request,first_name,last_name,email,username,password,question_one,answer_one,question_two,answer_two,customer)

        if flag:
            return render(request, "vendor_login.html")
        else:
            return render(request, "vendor_register.html")
    else:
        return render(request, "vendor_register.html")
def register_User(request,first_name,last_name,email,username,password,question_one,answer_one,question_two,answer_two,user):
    try:
        validateEmail(email)
        new_user = Fquestion.objects.create(question_one=question_one, answer_one=answer_one, question_two=question_two, answer_two=answer_two,
                             username=username, password=password, last_name= last_name, first_name= first_name
                             ,is_vendor=user, email=email)
        new_user.set_password(password)
        new_user.save()
        return True
    except Exception as error:
        messages.warning(request,error)
        return False