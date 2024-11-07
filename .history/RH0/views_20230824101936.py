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



def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        uploaded_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        saved_file = fs.save(uploaded_file.name, uploaded_file)

        # Extract text from the PDF file
        pdf_path = fs.url(saved_file)[1:]  # Remove the leading '/'
        pdf_text = extract_text_from_pdf(pdf_path)  # Call the function to get the actual PDF text
        return render(request, 'base.html', {'pdf_text': L0})
    
    return render(request, 'base.html')

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
import spacy
def nlp_txt(text):
    nlp=spacy.load('../output/model-best')
    doc=nlp(cv)
    Names=[]
    S=[]
    Links=[]
    for ent in doc.ents:
        if ent.label_== 'NAME':Names+=[ent.text]
        elif ent.label_== 'LINKEDIN LINK':Links+=[ent.text]
        elif ent.label_== 'SKILLS':S+=[ent.text.lower()]
    L=[Names,S,Links]
    return L

    
