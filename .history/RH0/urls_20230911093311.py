
from django.urls import path
from RH0 import views
from .views import entities
from .views import upload_zip

urlpatterns=[
    path('',views.index,name='RH0'),
    path('about',views.about,name='about'),
    path('upload_pdf', entities, name='upload_pdf'),
    path('upload_zip', upload_zip, name='upload_zip'),
    path('job_desc', views.job_desc, name='job_desc'),


]