from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return render(request,'base.html')

def about(request):
    return HttpResponse('this about')

from django.shortcuts import render, redirect
from RH0.forms import UploadFileForm
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import PyPDF2

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
import spacy
from bs4 import BeautifulSoup
import requests
import re

from .NLP import get_entities
nlp=spacy.load('./output/model-best')
GM = spacy.load("en_core_web_lg")


def pdf_to_text(input_file):
    i_f = open(input_file,'rb')
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr,retData, laparams= LAParams())
    interpreter = PDFPageInterpreter(resMgr,TxtConverter)
    for page in PDFPage.get_pages(i_f):
        interpreter.process_page(page)

    txt = retData.getvalue()
    return(txt)
def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        uploaded_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        saved_file = fs.save(uploaded_file.name, uploaded_file)

        # Extract text from the PDF file
        pdf_path = fs.url(saved_file)[1:]  # Remove the leading '/'
        pdf_text = pdf_to_text(pdf_path)
        ent=get_entities(pdf_text,nlp,GM)# Call the function to get the actual PDF text
        return render(request, 'upload_pdf.html', {'pdf_text': ent})
    return render(request, 'upload_pdf.html')

from django.http import HttpResponseRedirect
import zipfile
import os

def upload_zip(request):
    if request.method == 'POST' and request.FILES.get('zip_file'):
        uploaded_zip = request.FILES['zip_file']
        fs = FileSystemStorage()

        # Save the uploaded zip file
        saved_zip = fs.save(uploaded_zip.name, uploaded_zip)
        zip_path = fs.url(saved_zip)[1:]  # Remove the leading '/'

        # Extract the zip file
        extract_folder = 'extracted_files/'
        os.makedirs(extract_folder, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

        # Process extracted files
        extracted_files = os.listdir(extract_folder)
        pdf_texts = []
        for file_name in extracted_files:
            file_path = os.path.join(extract_folder, file_name)
            if file_name.endswith('.pdf'):
                pdf_text = extract_text_from_pdf(file_path)
                ents=get_entities(pdf_text,nlp,GM)
                pdf_texts.append(ents)

        # Clean up: remove extracted files and zip
        for file_name in extracted_files:
            os.remove(os.path.join(extract_folder, file_name))
        os.rmdir(extract_folder)
        os.remove(zip_path)

        return render(request, 'base.html', {'pdf_texts': pdf_texts})

    return render(request, 'base.html', {'pdf_texts': []})


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

