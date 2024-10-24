import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from ...config import getConfig

config = getConfig()

def toHTML(m,footer=None):
    o = "<div>\n"
    o += "<br/>\n".join(m.split("\n"))
    o += "\n</div>"
    o+="""
<div>
<hr />"""
    if footer:
        return o+"<br/>\n".join(footer.split("\n"))
    for i in config['scores']:
        sc = config['scores'][i]
        o+=f"{i.upper()} : {sc}<br/>"
    o+="</div>"
    return o

def try_login():
    myEmail = config['personal']['email']
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    password = config['personal']['password']
    server = smtplib.SMTP(smtp_server,smtp_port)
    server.ehlo()
    server.starttls()
    server.login(myEmail, password)
    server.quit()

#last_email = None
servers = {}
#save all emails
def send_email(txt_msg,subject,to_mail,cf=None):
    global servers
    if cf:
        html = toHTML(txt_msg,cf['footer'])
        myEmail = cf['email']
        password = cf['password']
        cv_location = cf['cv_location']
    else:
        html = toHTML(txt_msg)
        myEmail = config['personal']['email']
        password = config['personal']['password']
        cv_location = config['personal']['loc_cv']
    #print(cf)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    

    msg = MIMEMultipart('alternative')
    #msg = MIMEText(msg, 'html')
    msg["subject"] = subject
    msg["From"] = myEmail
    msg["To"] = to_mail
    part1 = MIMEText(txt_msg, 'plain')
    part2 = MIMEText(html, 'html')

    #print(config['personal']['loc_cv'])
    with open(cv_location, "rb") as f:
        #attachment
        part3 = MIMEApplication(
                    f.read(),
                    Name='CV.pdf'
                )
    msg.attach(part1)
    msg.attach(part2)
    msg.attach(part3)

    server = servers.get(myEmail)
    if not server:
        server = smtplib.SMTP(smtp_server,smtp_port)
        server.ehlo()
        server.starttls()
        last_email=myEmail
        server.login(myEmail, password)
        servers[myEmail]=server
    server.send_message(msg)
    return True
    #server.quit()
    #logg("Successfully sent email")
