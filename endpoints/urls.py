from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('change_statue/<esp_id>', views.change_statue,name='change_statue'),
    path('api/login', views.login_view, name='login'),
    path('api/test', views.test_view, name='test'),

]
