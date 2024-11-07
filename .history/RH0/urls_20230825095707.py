
from django.urls import path
from RH0 import views
from .views import upload_pdfs

urlpatterns=[
    path('',views.index,name='RH0'),
    path('about',views.about,name='about'),
    path('upload-pdf', upload_pdfs, name='upload_pdf'),

]