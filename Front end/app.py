from flask import Flask, render_template, flash, redirect, url_for, session, request, abort
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import requests
import json
import os
from werkzeug.utils import secure_filename
import logging
import time
from config import *
from flask_session import Session
from flask_cors import CORS, cross_origin

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}



app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'XSSDSDDD12323233333'
app.config['SESSION_TYPE'] = 'filesystem'


Session(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

@app.route('/')
@cross_origin()
def home():
    return render_template('home.html')


@app.route('/dashboardt',methods=['GET','POST'])
def dasht():
    if session.get("login",None) is True:
        return render_template('dashboard-t.html')
    else:
        return render_template('login.html')
        
@app.route('/login', methods=['GET','POST'])
def login():
    
    if request.method == 'POST':
        author_name = request.form['author_name']
        author_id = request.form['author_id']
        print(author_id)
        if author_name ==  '' or author_id == '':
            return render_template('login.html')
        app.logger.info("{},{}".format(author_name,author_id))
        headers = {'Content-type':'application/json'}
        data= {"author_name": author_name,"author_id":author_id}
        out = requests.post(backend_api+"/login", data=json.dumps(data), headers=headers)
        data = out.json()
        app.logger.info(type(data))
        if data["authorize"]:
            app.logger.info('TOKEN MATCHED')
            session['author_name'] = author_name
            session['author_id'] = author_id
            session['login'] = True
            return render_template('dashboard-t.html')
        else:
            app.logger.info('INCORRECT AUTHOR/AUTHOR ID')
       
    return render_template('login.html')
    

@app.route('/logout')
def logout():
    session.pop('author_name', None)
    session.pop('author_id', None)
    session.pop('login', None)
    return redirect(url_for('login'))

@app.route('/upload')
def upload():
   return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #print("inside")
            data = {"Author":session['author_name'], "AuthorID":session['author_id']}
            files = {
                'data': (None,json.dumps(data), 'application/json'),
                'file': file.read()
            }
                
                
            if filename.split('.')[-1] == "pdf":
                out = requests.post(textingester, files=files)
            else:
                
                out = requests.post(fileupload+'/uploadFile', files=files)
                print(out.json())
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("File uploaded successfully!", "info")
        else:
            flash("File didn't upload successfully.", "info")
    return render_template('dashboard-t.html')

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/updation', methods=['GET', 'POST'])
def update_file():
    if request.method == 'POST':
        file_id = request.form.get("fileid")

        
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file.filename.split(".")[-1] == "txt":
            data = {"Author":session['author_name'], "File_ID": file_id}
            files = {
            'data': (None,json.dumps(data), 'application/json'),
            'file': file.read()
            }
    
            out = requests.post(fileupload+'/update', files=files)
            print(out.json())
            flash("File updated successfully!", "info")
        else:
            flash("File didn't update successfully.", "info")
    return render_template('dashboard-t.html')

@app.route('/search')
def search_keyword():
    return render_template('search.html')

@app.route('/display', methods=['GET', 'POST'])
def displaydata():

    if request.method == 'POST':

        key = request.form.get("q",None)
        if key == None:
            return key
        data = {"Author": session['author_name'], "AuthorID": session['author_id'], "keyword": key}
        header_conf = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(backend_api+"/keywordSearch", data=json.dumps(data), headers=header_conf)
        output = response.json()
        print(output)
        res = output["file_id"]
        access = output['access_id']

            
        return render_template('search-result.html', value=key, dl=len(res), data=res, acces=access)

@app.route('/display/<string:id>/')
def displaydata2(id):
    data = {"Author": session['author_name'], "AuthorID": session['author_id'], "FILE_ID": id}
    logging.info("Display payload {}".format(data))
    header_conf = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(backend_api+"/getText", data=json.dumps(data), headers=header_conf)
    output = response.json()
    print(output)
    res = output["content"][0]
    text = res['text']
    return render_template('search-result2.html',  data=text)

@app.route('/registerform', methods=['GET','POST'])
def regform():
    if request.method == 'POST':
        if request.form.get("author_name") == "":
            return render_template('register.html')
        key1 = request.form.get("author_name")
       
        data = {"author_name": key1}
        header_conf = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(backend_api+"/signup", data=json.dumps(data), headers=header_conf)
        
        rest = response.json()
        return render_template('cred.html', author_name=key1, author_id=rest['author_id'])

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':    
    app.run(host="0.0.0.0", port=80, debug=True)
