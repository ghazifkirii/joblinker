
from .NLP import get_entities
from .views import extract_text_from_pdf,match_CJ

from django.http import HttpResponseRedirect
import zipfile
import os
import threading
from django.shortcuts import render,HttpResponse
from django.core.files.storage import FileSystemStorage
import io
import spacy
from bs4 import BeautifulSoup
import requests
nlp=spacy.load('./output/model-best')
GM = spacy.load("en_core_web_lg")
from django.shortcuts import render, redirect  # Import the 'redirect' function

def process_pdf_files(extracted_files, extract_folder, nlp, GM,job):
    pdf_texts = []
    for file_name in extracted_files:
        file_path = os.path.join(extract_folder, file_name)
        if file_name.endswith('.pdf'):
            pdf_text = extract_text_from_pdf(file_path)
            ents = get_entities(pdf_text, nlp, GM)
            ents.append(match_CJ(pdf_text, job, ents))
            pdf_texts.append(ents)

    return pdf_texts


def result_page(request):
    pdf_texts = request.session.get('pdf_texts', [])
    pdf_filenames = request.session.get('pdf_filenames', [])  # Retrieve the list of PDF filenames
    return render(request, 'result_zip.html', {'pdf_texts': pdf_texts, 'pdf_filenames': pdf_filenames})

def upload_zip(request):
    if request.method == 'POST' and request.POST.get('job', ''):
            job = request.POST.get('job', '')  # Use a default value if 'job' is not in POST data
    else: 
        ent=[]
        pdf_text=''
        job_text = ''
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
        # Process extracted files using multi-threading
        extracted_files = os.listdir(extract_folder)
        pdf_filenames = [filename for filename in extracted_files if filename.lower().endswith('.pdf')]

        num_threads = min(len(extracted_files), os.cpu_count())
        threads = []
        pdf_texts = []

        def process_thread(thread_batch):
            return process_pdf_files(thread_batch, extract_folder, nlp, GM,job)

        for i in range(0, len(extracted_files), num_threads):
            thread_batch = extracted_files[i: i + num_threads]
            thread = threading.Thread(target=lambda batch=thread_batch: pdf_texts.extend(process_thread(batch)))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Clean up: remove extracted files and zip
        for file_name in extracted_files:
            os.remove(os.path.join(extract_folder, file_name))
        os.rmdir(extract_folder)
        os.remove(zip_path)

        # Store the result in a session variable
        request.session['pdf_texts'] = pdf_texts
        request.session['pdf_filenames'] = pdf_filenames  # Store the list of PDF filenames

        return redirect('result_zip')  # Redirect to the result page

    return render(request, 'base.html', {'pdf_texts': []})

# Add this view to serve PDF files
def download_pdf(request, pdf_filename):
    pdf_path = os.path.join('extracted_files', pdf_filename)  # Replace with the actual path to your PDFs
    with open(pdf_path, 'rb') as pdf_file:
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
        return response