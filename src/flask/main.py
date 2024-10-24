#!/usr/bin/env python3

import uuid
from flask import Flask, session, render_template, request, redirect, url_for
from waitress import serve
import os
import configparser
from ..scholar import get_prof_datas
from ..crawler import crawl_info
from ..loaddocs import docs_to_text,get_documents
from ..createmail import docs_to_email
from ..sendmail import send_email
from ..config import getConfig
config = getConfig()

app = Flask(__name__)
app.secret_key = 'supersecretkeyxxxwwwrrrtttyyx'  # Needed for session handling, keep it secret

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for saving user info
@app.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    if request.method == 'POST':
        if request.form['action'] == 'SaveInfo':
            session['username'] = request.form['username']
            session['email'] = request.form['email']
            session['password'] = request.form['password']
            session['cv_location'] = request.form['cv_location']
            session['university'] = request.form['university']
            session['footer'] = request.form['footer']
            session['department'] = request.form['department']  # Add this line
            return redirect(url_for('profinfo'))
        
        elif request.form['action'] == 'UploadCV':
            if 'cv_file' in request.files:
                cv_file = request.files['cv_file']
                if cv_file.filename != '':
                    # Create the directory if it doesn't exist
                    os.makedirs('./assets/configs', exist_ok=True)
                    
                    # Get the file extension
                    file_name, file_extension = os.path.splitext(cv_file.filename)
                    
                    # Create a filename using the username (if available) or a random UUID
                    base_filename = file_name
                    filename = f"{base_filename}{file_extension}"
                    
                    # Check if file already exists and generate a new name if it does
                    filepath = os.path.join('assets/docs', filename)
                    counter = 1
                    while os.path.exists(filepath):
                        filename = f"{base_filename}_{counter}{file_extension}"
                        filepath = os.path.join('assets/docs', filename)
                    
                    # Save the file
                    cv_file.save(filepath)
                    
                    # Update the cv_location in the session
                    session['cv_location'] = filepath
                    
                    print(f"CV file saved: {filepath}")
                else:
                    return render_template('message.html', message="No file selected")
            else:
                return render_template('message.html', message="No file part in the request")
        else:
            session['user'] = request.form['username']
            filepath = f"./assets/configs/{request.form['username']}.ini"
            if os.path.exists(filepath):
                config = configparser.ConfigParser()
                config.read(filepath)
                session['username'] = config['personal']['NAME']
                session['email'] = config['personal']['EMAIL']
                session['password'] = '@useConfig'
                session['cv_location'] = config['personal']['LOC_CV']
                session['university'] = config['personal']['UNI']
                session['department'] = config['personal'].get('DEPARTMENT', "Master's in Civil Engineering")  # Add this line
                o=''
                for i in config['scores']:
                    sc = config['scores'][i]
                    o+=f"{i.upper()} : {sc}\n"
                session['footer'] = o.rstrip()
            else:
                return render_template('message.html', message="Config file not found")
        return redirect(url_for('userinfo'))
    username = session.get('username', '')
    email = session.get('email', '')
    password = session.get('password', '')
    cv_location = session.get('cv_location', '')
    university = session.get('university', '')
    footer = session.get('footer', '')
    department = session.get('department', '')  # Add this line
    return render_template('userinfo.html', username=username, email=email, password=password,
                           cv_location=cv_location, university=university, footer=footer,
                           department=department)  # Add department here

# Route to view details
@app.route('/profinfo', methods=['GET', 'POST'])
def profinfo():
    if request.method == 'POST':
        session['prof_name'] = request.form.get('prof_name').strip()
        session['prof_email'] = request.form.get('prof_email').strip()
        session['prof_profile'] = request.form.get('prof_profile').strip()
        session['prof_university'] = request.form.get('prof_university').strip()
        return redirect(url_for('profload'))
    
    prof_name = session.get('prof_name', '')
    prof_email = session.get('prof_email', '')
    prof_profile = session.get('prof_profile', '')
    prof_university = session.get('prof_university', '')
    prof_index = session.get('prof_index', '')
    
    return render_template('profinfo.html', 
                           prof_name=prof_name,
                           prof_email=prof_email,
                           prof_profile=prof_profile,
                           prof_university=prof_university,
                           prof_index=prof_index)

def get_prof_from_session(session):
    prof = {
        'name': session.get('prof_name', ''),
        'position': session.get('prof_position', ''),
        'university': session.get('prof_university', ''),
        'bio': session.get('prof_profile', ''),  
        'ref': 'manual',
        'email': session.get('prof_email', '')
    }
    return prof

def get_user_id(session):
    user_id = session.get('kuser_id')
    if user_id:
        return user_id
    else:
        # Generate a new user_id if not available in session
        user_id = str(uuid.uuid4())
        session['kuser_id'] = user_id
        return user_id

#to store large contents instead of from session
secondary_storage = {}

def get_secondary_storage(user_id):
    if user_id not in secondary_storage:
        secondary_storage[user_id] = {}
    return secondary_storage[user_id]

@app.route('/profload', methods=['GET', 'POST'])
def profload():
    #session['actions_log'] = ''
    user_id = get_user_id(session)
    secondary_storage = get_secondary_storage(user_id)
    #print(secondary_storage)
    actions_log = secondary_storage.get('actions_log', '')

    if request.method == 'POST':
        prof_docs = secondary_storage.get('prof_docs', [])
        r=None
        prof = get_prof_from_session(session)
        if 'scholar_email' in request.form:
            scholar_email = request.form['scholar_email']
            prof['email'] = scholar_email
            r=get_prof_datas(prof)
            if r:
                actions_log += f"Successfully downloaded data for {scholar_email} from Google Scholar<br/>\n"
            else:
                actions_log += f"Failed to download data for {scholar_email} from Google Scholar<br/>\n"
        elif 'profile_url' in request.form:
            profile_url = request.form['profile_url']
            prof['bio']=profile_url
            if 'single_page' in request.form:
                prof['single_page']=True
            r=crawl_info(prof)
            if r:
                actions_log += f"Successfully downloaded data from profile: {profile_url}<br/>\n"
            else:
                actions_log += f"Failed to download data from profile: {profile_url}<br/>\n"
        #print('update')
        if r:
            secondary_storage['prof_docs']=prof_docs+r
        #print(session['prof_docs'])
        secondary_storage['actions_log'] = actions_log
        #print(secondary_storage)
    
    if actions_log=='':
        actions_log='Start downloading datas below.'
    return render_template('profload.html', 
                           actions_log=actions_log,
                           prof_email=session.get('prof_email', ''),
                           prof_profile=session.get('prof_profile', ''))

path = config['directories']['PERSIST_PATH']
@app.route('/email', methods=['GET', 'POST'])
def email():
    user_id = get_user_id(session)
    secondary_storage = get_secondary_storage(user_id)
    if request.method == 'POST':
        if request.form['action'] == 'CreateMail':
            # Generate mail content
            pcs = secondary_storage.get('prof_docs')
            if not pcs:
                return render_template('message.html', message="No documents found, please load professor's data first")
            docs = get_documents(pcs)
            fd = docs_to_text(docs)
            prof = get_prof_from_session(session)
            customConfig = {
                'name': session.get('username', ''),
                'university': session.get('university', ''),
                'department': session.get('department', '')  # Add this line
            }
            mail = docs_to_email(fd, prof, customConfig)
            secondary_storage['mail_subject'] = mail[0]
            secondary_storage['mail_body'] = mail[1]
            # Log the generated email
            log_file_path = os.path.join(path, 'generatedMails.txt')
            with open(log_file_path, 'a') as log_file:
                log_file.write(f"Subject: {secondary_storage['mail_subject']}\n")
                log_file.write(f"Body:\n{secondary_storage['mail_body']}\n")
                log_file.write("-" * 50 + "\n")  # Separator for readability
            #print(session['user_id'])
            return redirect(url_for('email'))
        elif request.form['action'] == 'SendMail':
            # Send the email
            mail_subject = request.form['email_subject']
            mail_body = request.form['email_body']
            recipient = session.get('prof_email', '')
            if recipient=='':
                return render_template('message.html', message="Please enter a recipient email in professor tab.")
            if mail_subject=='' or mail_body=='':
                return render_template('message.html', message="Please enter a subject and body for the email.")
            if recipient:
                cf = {
                    'footer': session.get('footer', ''),
                    'email': session.get('email', ''),
                    'password': session.get('password', ''),
                    'cv_location': session.get('cv_location', '')
                }
                if cf['password'] == '@useConfig':
                    config = configparser.ConfigParser()
                    config.read(f"./assets/configs/{session['user']}.ini")
                    if 'personal' not in config:
                        return render_template('message.html', message="Looks like the server reset, causing loss of information. Please re-enter your information.")
                    if 'PASSWORD' in config['personal']:
                        cf['password'] = config['personal']['PASSWORD']
                    else:
                        return render_template('message.html', message="Looks like the server reset, causing loss of information. Please re-enter your information.")
                if not cf['cv_location'].startswith('assets/docs/'):
                    return render_template('message.html', message="Invalid CV location")
                log_file_path = os.path.join(path, 'sentMails.txt')
                #sent mail log
                with open(log_file_path, 'a') as log_file:
                    log_file.write(f"Subject: {mail_subject}\n")
                    log_file.write(f"Body:\n{mail_body}\n")
                    log_file.write("-" * 50 + "\n")  # Separator for readability

                if send_email(mail_body, mail_subject, recipient, cf):
                    return redirect(url_for('done'))
                else:
                    return render_template('message.html', message="Failed to send email")
            else:
                return render_template('message.html', message="No recipient email found in session")
    return render_template('email.html', mail_subject=secondary_storage.get('mail_subject', ''), mail_body=secondary_storage.get('mail_body', ''))

@app.route('/done')
def done():
    return render_template('done.html')

# Route to clear session
@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    user_id = get_user_id(session)
    if secondary_storage:
        if secondary_storage.get(user_id):
            del secondary_storage[user_id]
    return redirect(url_for('home'))

import json
@app.route('/nextprof')
def nextprof():
    user_id = get_user_id(session)
    secondary_storage = get_secondary_storage(user_id)
    if not secondary_storage.get('prof_list'):
        current_file = os.path.join(path, 'current')
        with open(current_file, 'r') as f:
            current_name = f.read()
        current_file_uni = os.path.join(path, f'profs({current_name})')
        with open(current_file_uni, 'r') as f:
            current_uni = json.load(f)
        secondary_storage['prof_list']=current_uni
        if not session.get('prof_index'):
            session['prof_index']=-1
    session['prof_index']+=1
    index=session['prof_index']
    if index>=len(secondary_storage['prof_list']):
        session['prof_index']=-1
        return render_template('message.html', message="List is completed, restating counting")
    session['prof_name']=secondary_storage['prof_list'][index]['name'].strip()
    session['prof_email']=secondary_storage['prof_list'][index]['email'].strip()
    session['prof_profile']=secondary_storage['prof_list'][index].get('bio','').strip()
    session['prof_university']=secondary_storage['prof_list'][index].get('university','').strip()
    return redirect(url_for('profinfo'))

# Route to clear session
@app.route('/clearprof')
def clearprof():
    #session.clear()  # Clear session data
    user_id = get_user_id(session)
    session['prof_name']=''
    session['prof_email']=''
    #session['prof_position']=''
    session['prof_profile']=''
    #session['prof_university']=''
    if secondary_storage:
        if secondary_storage.get(user_id):
            del secondary_storage[user_id]
    return redirect(url_for('profinfo'))

from datetime import datetime
@app.route('/submit_suggestion', methods=['POST'])
def submit_suggestion():
    suggestion = request.form.get('suggestion')
    if suggestion:
        log_file_path = os.path.join(path, 'suggestions.txt')
        with open(log_file_path, 'a') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {suggestion}\n")
        return render_template('message.html', message='Thank you for your suggestion!')
    else:
        return render_template('message.html', message='Please enter a suggestion before submitting.')

def main(debug=False):
    if debug:
        app.run(debug=True)
    else:
        serve(app, host='0.0.0.0', port=5000)
        

if __name__ == '__main__':
    main()
