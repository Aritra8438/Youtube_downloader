from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('choose/',views.choose,name='choose'),
    path('getFile/',views.getFile,name='getFile'),
]