
from django.urls import path
from RH0 import views

urlpatterns=[
    path('',views.index,name='RH0'),
    path('about',views.about,name='about'),
    path('upload', views.upload_file, name='upload_file'),

]