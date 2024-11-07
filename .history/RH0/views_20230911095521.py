from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
def index(request):
    return render(request,'base.html')

def about(request):
    return HttpResponse('this about')

from RH0.forms import UploadFileForm
import PyPDF2
from django.core.files.storage import FileSystemStorage

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
        ent=get_entities(pdf_text,nlp,GM)
        return ent
    else: return []
    
def entities(request):
    ents=upload_pdf(request)
    if len(ents)>0:
        return render(request, 'upload_pdf.html', {'pdf_text': ents})
    else:
        return render(request, 'upload_pdf.html')
    
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

from django.shortcuts import render
from django.http import HttpResponse

def job_desc(request):
    if request.method == 'POST':
        job_text = request.POST.get('job', '')  # Use a default value if 'job' is not in POST data
    else:
        job_text = ''
    return job_text

def job_html(request):
    if request.method == 'POST':
        return render(request, 'upload_pdf.html', {'job_text': job_desc(request)})
    else:
        return render(request, 'upload_pdf.html')
    

    
    