
from django.urls import path
from RH0 import views
from RH0 import views_zip

from .views import entities
from .views_zip import upload_zip

urlpatterns=[
    path('',views.index,name='RH0'),
    path('about',views.about,name='about'),
    path('upload_pdf', entities, name='upload_pdf'),
    path('upload_zip', upload_zip, name='upload_zip'),
    path('result_zip', views_zip.result_page, name='result_zip'),

]