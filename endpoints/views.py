from secrets import token_urlsafe

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from endpoints.models import Esp


# Create your views here.

@csrf_exempt
def index(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            token = token_urlsafe(16)
            esp = Esp.objects.filter(user=request.user).first()
            esp.token = token
            esp.save()
            return render(request, 'endpoints/index.html', {"token": token})
    if request.method == 'POST':
        Esp.objects.all().update(status=not Esp.objects.all()[0].status).save()
    else:
        esps = Esp.objects.all()
        return render(request, 'endpoints/index.html', {'esps': esps})


@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid username or password.'
    else:
        error_message = None

    context = {'error_message': error_message}
    return render(request, 'endpoints/login.html', context)


@csrf_exempt
def change_statue(request, esp_id):
    esp = get_object_or_404(Esp, id=esp_id)
    esp.status = not bool(esp.status)
    esp.save()
    return JsonResponse({'status': 'success'})


def test_view(request):
    return JsonResponse({'status': request.user.is_authenticated})
