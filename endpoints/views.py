from secrets import token_urlsafe

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from endpoints.models import Esp


# Create your views here.

@csrf_exempt
def index(request):
    if not request.user.is_anonymous:
        if request.method == 'GET':
            token = token_urlsafe(16)
            esp = Esp.objects.filter(user=request.user).first()
            esp.token = token
            esp.save()
            return render(request, 'endpoints/index.html', {"token": token})
    if request.method == 'POST':
        Esp.objects.all().update(status=not Esp.objects.all()[0].status).save()
    else:
        return render(request, 'endpoints/index.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password.'
    else:
        error_message = None

    context = {'error_message': error_message}
    return render(request, 'endpoints/login.html', context)