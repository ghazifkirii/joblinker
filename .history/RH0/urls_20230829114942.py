
from django.urls import path
from .views import upload_pdf
from .views import upload_zip

urlpatterns=[
    path('',views.index,name='RH0'),
    path('about',views.about,name='about'),
    path('upload-pdf', upload_pdf, name='upload_pdf'),
    path('upload_zip', upload_zip, name='upload_zip'),

]