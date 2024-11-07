
import spacy
from bs4 import BeautifulSoup
import requests
import re
import spacy

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

def get_entities(cv,nlp,GM):
    doc=nlp(cv)
    Names=[]
    S=[]
    Links=[]
    for ent in doc.ents:
        if ent.label_== 'NAME':Names+=[ent.text]
        if ent.label_== 'LINKEDIN LINK':Links+=[ent.text]
        if ent.label_== 'SKILLS':S+=[ent.text.lower()]
    doc0 = GM(cv)
    mail=''
    git=''
    git_data=''
    for token in doc0:
        if '@' in token.text :
            if is_valid_email(token.text):mail=token.text
        elif 'hub.com/' in token.text :
            git=valid_url(token.text)
            git_data=git_scrap(git)
    name=RV(Names,mail)
    link=RV(Links,mail)
    for s in skills:
        if s in process_resume(cv):S+=[s]
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

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("Maite89/Roberta_finetuning_semantic_similarity_stsb_multi_mt")
def Corr(lis,mail):
    e1=model.encode(mail,convert_to_tensor=True)
    Sim=[]
    for n in lis:
        e2=model.encode(n.lower(),convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(e1, e2)
        Sim.append(float(similarity[0][0]))
    out=lis[np.array(Sim).argmax()]
    return out