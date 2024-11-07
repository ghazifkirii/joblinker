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
        if pdf_text.strip():
            ent = get_entities(pdf_text, nlp, GM)
        else:
            ent = []        
    else:
        ent=[]
        pdf_text=''
        job_text = ''
    if request.method == 'POST' and request.POST.get('job', ''):
        job_text = request.POST.get('job', '')  # Use a default value if 'job' is not in POST data
    else: 
        ent=[]
        pdf_text=''
        job_text = ''
    return [ent,job_text,pdf_text]    
    
def process_resume(cv):
    processed_token = []
    for token in cv.split():
        token = ''.join(e.lower() for e in token)
        processed_token.append(token)
    return ' '.join(processed_token)
skills=['ESP32','UNITY','DATA VISUALIZATION','ANDROID STUDIO','FIREBASE','JAVA','DART','FLUTTER','REACT JS','HTML','CSS' 'C','C++','C#','Bash','Assembly','VHDL','Phython','JS','SQL','Arduino UNO',
        'STM32','FPGA','React JS','Flask','Tikinter','Flutter','VS CODE','Git','GitHUB','Arduino IDE','Keil','Kuartus','STM32Cubemx','MySQL','Spring','Angular','.NET','Flutter','NOSQL','NodeJs','Javascript',
        'Flutter','NodeJs','Data Mining','angular','springboot','java','typescript','.NET','php','sass','mariaDB','graphql','mysql','JDBC','IntellijIDEA','WebStorm','git','AdobePhotoshop','VSCode','Angular',
       'symfony','bootstrap','sqlite','NLP','Prompt engineering','Flask','reactJS','Vosk','Deep Learning','Python','ROS','Deep Learning','Django Framework','Anaconda Jupiter','SQL Management Server',
        'SQL Data Tools','power BI','Django','SQL','Matlab','ASP.NET','Flask','Qt','Oracle','mySQL','MongoDB','Computer Vision','Machine Learning','DeepLearning','OpenCV','Raspberry Pi','Raspbian',
        'L298n','Arduino','MIT App Inventor','Proteus 8 Professional','C#','ASP.NET','Visual Studio','Codeblocks','Object-Oriented Programming','Qt','Git/Github','ReactJS'
        "Python", "Java", "C++", "JavaScript", "C#",'C', "Ruby", "PHP", "Swift", "Go", "Rust", "Kotlin", "SQL", "HTML","CSS", "R", "MATLAB", "TypeScript", "Scala", "Perl", "Shell scripting (Bash)",
         "Sorting algorithms", "Graph algorithms", "Dynamic programming", "Hashing", "Linked lists", "Trees (binary trees, AVL trees, etc.)", "Stacks and queues", "Hash tables", "React", "Angular",
         "Vue.js", "Node.js", "Express.js", "Django", "Flask", "ASP.NET Core", "HTML5", "CSS3", "Android (Java/Kotlin)", "iOS (Swift)", "React Native", "Flutter", "MySQL", "PostgreSQL", "MongoDB",
         "SQLite", "Oracle", "Microsoft SQL Server", "Amazon Web Services (AWS)", "Microsoft Azure", "Google Cloud Platform (GCP)", "Hadoop", "Spark", "Apache Kafka", "Apache Flink", "Tableau",
         "Power BI", "Docker", "Kubernetes", "Jenkins", "Travis CI", "CircleCI", "GitLab CI/CD", "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "OpenCV", "Unity", "Unreal Engine", "Godot",
         "TCP/IP", "HTTP/HTTPS", "DNS", "Load Balancing", "Linux", "Windows", "macOS", "Git", "SVN", "Mercurial", "Ethereum", "Hyperledger", "VirtualBox", "VMware", "Arduino", "Raspberry Pi",'keras',
         'pil','tensorflow','pandas','numpy','spacy','hugging face','airflow','Git','Jenkins','IntelliJ IDEA','Eclipse','Sublime Text','PyCharm','Postman','Selenium','Apache Maven','Gradle','OOP',
        'Python','Java','C/C++','Matlab','VHDL','Database management','MySQL','SQL','HTML5','CSS3','JavaScript','windows','Linux' ,'GitHub','stm32','arduino','Raspberry','vs code','PyCharm',
        'Eclipse', 'Google Colaboratory', 'Jupyter','Terraform', 'IaC', 'Packer', 'Ansible', 'AWS', 'containers', 'K8s', 'EKS', 'Java','Spring', 'Jenkins', 'Gitlab', 'DRP'
        'Grafana','Prometheuse']

def match_CJ(cv,job,lt):
    #Match similarity
    Match_Test=[cv,job]
    cv=CountVectorizer()
    count_matrix=cv.fit_transform(Match_Test)
    Match=cosine_similarity(count_matrix)[0][1]
    #num skills
    ct=0
    for s in lt[-1]:
        if s in process_resume(job):ct+=1
    miss_sk=[]
    skills_job=[]
    for si in skills:
        si=si.lower()
        if si in process_resume(job) :
            skills_job+=[si]
            if si not in lt[-1]:miss_sk+=[si]
    return [Match,ct,miss_sk,skills_job]

def entities(request):
    ents=upload_pdf(request)
    M=match_CJ(ents[2],ents[1],ents[0])
    if len(ents)>0:
        return render(request, 'upload_pdf.html',  {'entities': ents[0], 'job_description': ents[1] ,'match':M})
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
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


    