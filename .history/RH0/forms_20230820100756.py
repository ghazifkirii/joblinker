from django import forms
from .models import UploadedFile

class UploadFileForm(forms.Form):
    file_field = forms.FileField()
