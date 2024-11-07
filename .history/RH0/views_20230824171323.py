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

nlp=spacy.load('./output/model-best')
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
        pdf_text = pdf_to_text(pdf_path)  # Call the function to get the actual PDF text
        L0=get_entities(pdf_text,nlp,GM,skills)        
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
#riguel names barch ne9sin (jareb model e5or) yelzem 95%
#riguel sracp mta3 em git jst rak tscrapi el popular
def get_entities(cv,nlp,GM,skills):
  doc=nlp(cv)
  Names=[]
  S=[]
  Links=[]
  for ent in doc.ents:
    if ent.label_== 'NAME':
      Names+=[ent.text]
    if ent.label_== 'LINKEDIN LINK':
      Links+=[ent.text]
    if ent.label_== 'SKILLS':
      S+=[ent.text.lower()]

  for s in skills:
    if s in process_resume(cv):
      S+=[s]
  return [name,git,git_data,link,mail,list(set(S))]
import re
def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email):
        return True
    else:
        return False
import requests
def valid_url(url):
  count=0
  for c in url:
    if '/' ==c:count+=1
  if count>3:
    url=url[:len(url)-url[::-1].index('/')]
  if url[:4]!='http':
    url='https://'+url
  if requests.get(url):return url
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

skills=[e.lower() for e in skills if e.isalnum()]
def RV(L,mail):
    if len(L)==0:N=''
    elif len(L)==1:N=L[0]
    else:N=Corr(L,mail)
    return(N)
#return all the reposities of github
def get_repos(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  repo_anchors = soup.select('a')
  repository_urls = [f"https://github.com{anchor['href']}" for anchor in repo_anchors]
  a_tag = soup.select('a')
  repos=[]
  for i in a_tag:
    repos+=[i.find('span', {'class': 'repo'})]
  non_none_indices = [index for index, item in enumerate(repos) if item is not None]
  rep=[a_tag[i] for i in non_none_indices]
  hrefs=[]
  for i in rep:
    soup = BeautifulSoup(str(i),'html.parser')
    tag_rep = soup.find('a')
    if tag_rep:
      hrefs+=['https://github.com'+tag_rep['href']]
  return(hrefs)
#get the number of contributions on github
def get_cont(url):
  response = requests.get(valid_url(url))
  soup = BeautifulSoup(response.content, 'html.parser')
  h2s = soup.select('h2',{'class':'f4 text-normal mb-2'})
  TT=[]
  for i in h2s:
    TT+=[i.text.replace('\n','').replace(' ','')]
    pattern = r'\d+'
  return([int(re.search(pattern, item).group()) for item in TT if re.search(pattern, item)][0])
#get languages of programmation of each repo
def get_langs(url):
  langs=[]
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  for i in soup.find_all('li',{'class':'d-inline'}):
    soup0 = BeautifulSoup(str(i),'html.parser')
    lang=soup0.find('span').text.replace('\n','')
    if 'Other' not in lang:
      langs+=[lang]
  return(langs)
#return all the languages
def all_langs(url):
  langs=[]
  for i in get_repos(url):
    langs+=[item.split('%')[0] for item in [re.sub(r'\d+\.\d+', '', item) for item in get_langs(i)]]
  return(langs)
def git_scrap(url):
  U=[]
  url=valid_url(url)
  U=[url,get_repos(url),get_cont(url),list(set(all_langs(url)))]
  return U
    
