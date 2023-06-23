from django.urls import path
from . import views

app_name = 'get_data'

urlpatterns = [
    path('', views.getdata, name='getdata'),
]
