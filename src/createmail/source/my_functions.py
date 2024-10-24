from langchain.prompts import ChatPromptTemplate
import random
from ...config import getConfig

config = getConfig()

def filter_placeholders(t):#if placeholder remove the whole sentence.
    st=0
    while True:
        brst = t.find('[',st)
        if brst==-1:
            break
        head = t[brst+1:brst+5]
        endss = t.find(']',brst)
        if head not in ['Your','your','Prof','prof','Univ','univ','Inse','inse','Rese','rese','ment','Ment','Spec','spec','brie','Brie']:
            st=brst+1
            continue
        #blacklist everything
        if head[0] in "0123456789":
            st=brst+1
            continue
        #if endss!=-1 and endss-brst>30:
        #    st=brst+1
        #   continue
        #lets assume it is always in mid, else we fail anyway dont worry
        ss1 = t.rfind('.',0,brst)
        ss2 = t.rfind('\n',0,brst)
        if ss1==-1:
            ss=ss2
        elif ss2==-1:
            ss=ss1
        else:
            ss = max(ss1,ss2)
        se1 = t.find('.',brst)
        se2 = t.find('\n',brst)
        if se1==-1:
            se=se2
        elif se2==-1:
            se=se1
        else:
            se = min(se1,se2)
        t=t[:ss]+t[se:]
    return t

MAX_LENGTH = 1000

prompt = ChatPromptTemplate.from_messages(
    [("system", 
      """Read the papers below and write email. 

Papers:\n\n{input}

are authored by provided professor.
Your task is to write a mail to professor on what you like about the given research topics from professor and express eagerness to learn. write to him/her on why you want to  learn, study on those topic. Dont make anything up. Dont forget to tell the professor that you have read some research based on given research.
You have no prior research experise nor doing any current research, but dont mention it. Make it fell more formal, include research titles and brief summary if possible but do not make any title on your own.
dont mention anthing about you. write long descriptions. mention thank you. it is 2024 now. i am student not researcher. make information about papers longer and detailed.

Professor Info:{prof_info}""")]
)

from ...loaddocs import prof_to_doc

KLIMIT = 15

#convert provided docs to snips
def docs_to_email(fd,prof,cf=None):
    if cf:
        university = cf['university']
        name = cf['name']
        department = cf['department']
    else:
        university = config['personal']['UNI']
        name = config['personal']['NAME']
        department = config['personal'].get('DEPARTMENT',"Master's degree in Civil Engineering")
    pinfo = prof_to_doc(prof)
    if len(fd)>15*MAX_LENGTH:
        fd=fd[-15*MAX_LENGTH:]#clamp it
    #logg(f'{len(fd)} characters used for summay')
    #create message
    #initial_message = chain.invoke({"input": fd,'prof_info': pinfo})
    p=prompt.format(input= fd,prof_info = pinfo)
    from ...genai.source import get_response
    initial_message = get_response(p)

    #logg('\nPatching mail.')
    #try finding subject
    subject_start = initial_message.find('Subject')
    mail_subject=None
    if subject_start!=-1:
        subject_start1 = initial_message.find(':')
        if subject_start1 == -1:
            subject_start1 = subject_start + 9
        else:
            subject_start1 += 2
        s_end = initial_message.find('\n', subject_start1)-1
        mail_subject = initial_message[subject_start1: s_end+1]
    if mail_subject:
        if len(mail_subject)>100:
            mail_subject=None
    if not mail_subject or '[' in mail_subject or ']' in mail_subject:# dont get [] in subject
        mail_subject = random.choice(['Intrest in Research','Intrest in Research','Exited to persue Masters and/or Phd under guidance',"Exploring Research Opportunities","Exploring Research Opportunities"])
    dloc = initial_message.find('Dear')
    initial_message = initial_message[dloc:]
    k = initial_message.find('finds you well.')
    if k == -1:
        p = initial_message.find(',')
        initial_message = initial_message[:p+3] + '\nI hope this message finds you well. I recently stumbled across your profile on the '+prof['university']+' website and was impressed by your researches. ' + initial_message[p+3:]
    else: 
        k=k+15
        initial_message = initial_message[:k] + ' I recently stumbled across your profile on the '+prof['university']+' website and was impressed by your researches. ' + initial_message[k+1:]
    p = initial_message.find('Thank')
    if p==-1:
        p=initial_message.find('Sincerely')
    #print(config)
    initial_message = initial_message[:p] + "As someone who has completed my undergraduate studies at the "+university+", Nepal, I would like to pursue a "+ department +""". As such, I am excited about the possibility of joining your research team because your research interests align closely with mine interests.

I am writing to inquire if there are any openings for graduate students to join your research team in the upcoming intake. It would be an honor for me to work under your guidance as a Research Assistant, either on your current project or any other similar projects. I am willing to work diligently and learn new skills as needed. I have attached my Curriculum Vitae for your review.
\nThank you for considering my application, and I look forward to hearing from you soon.

Sincerely,
"""+name
    
    return [mail_subject, filter_placeholders(initial_message)]

