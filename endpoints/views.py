import json
from secrets import token_urlsafe
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from endpoints.models import Esp


# Create your views here.

@csrf_exempt
def index(request):
    if request.user.is_authenticated:
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
        json_data = json.loads(request.body)
        # Access the JSON data like a Python dictionary
        username = json_data['username']
        password = json_data['password']
        print(username,password)
        user = authenticate(request, username=username, password=password)
        print(user.id)
        if user is not None:
            token = token_urlsafe(16)
            print(token)
            esp = get_object_or_404(Esp,id=user.id)
            esp.token = token
            esp.save()
            response_data = {'status': 'success', 'message': f'{token}'}
            return JsonResponse(response_data)
    else:
        # If the request method is not POST, return a JSON response with an error message
        response_data = {'status': 'error', 'message': 'Invalid request method'}
        return JsonResponse(response_data, status=405)


@csrf_exempt
def change_statue(request, esp_id):
    esp = get_object_or_404(Esp, id=esp_id)
    esp.status = not bool(esp.status)
    esp.save()
    return JsonResponse({'status': 'success'})


def esp_token(request):
    token = token_urlsafe(16)
    esp = get_object_or_404(Esp, user=request.user)
    esp.token = token
    esp.save()
    return JsonResponse({'token': token})
