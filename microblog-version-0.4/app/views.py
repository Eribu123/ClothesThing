import os
import sys
from flask import Flask, flash,  request, redirect, url_for, send_from_directory, render_template
from app import app
from .forms import LoginForm
from werkzeug.utils import secure_filename
import DataTracking as DT
import SeperationAL as SepAl
from PIL import Image
import time

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/get',methods= ['POST'])
def getRoute():
    pass
aFileName=''
afile=None

def install_secret_key(app, filename='secret_key'):
    filename = os.path.join(app.instance_path, filename)
    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print 'Error: No secret key. Create it with:'
        if not os.path.isdir(os.path.dirname(filename)):
            print 'mkdir -p', os.path.dirname(filename)
        print 'head -c 24 /dev/urandom >', filename
        sys.exit(1)

install_secret_key(app, filename='secret_key')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
       
       
        # check if the post request has the file part
        print (request.files)
        print 'oisdjsadfilnfsd'
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        elif file and allowed_file(file.filename):
            aFileName= filename = secure_filename(file.filename)
            afile= file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print 'oijadsfoiasdfioasdiopfasdiofjs'
            # return redirect(url_for('uploaded_file', filename=filename))

        print 'oijadsfoiasdfioasdiopfasdiofjs'
        time.sleep(2)
        username=request.form['username']
        path="/home/ubuntu/ClothesThing/microblog-version-0.4/uploads/"+request.form['fname']
        print 'o'
        
        print(username, path)
        DT.InputData(username,path,SepAl.classify(Image.open(path)))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <h3>give us a UsrName</h3>
    <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
            <input type=submit value=Upload>
    </form>
    <form>
  Name: <input type="text" name="name" id="name" value="" />
    <input type="submit" value="submit" />
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    pass

    return '''
    <!doctype html>
    <title>Uploaded</title>
    <h1>Uploaded</h1>
    '''


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
@app.route('/data', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def test():
    pass
    # DT.InputData('ex1','/Users/kyle/Desktop/image1.jpeg',SepAl.classify(Image.open('/Users/kyle/Desktop/image1.jpeg')))


    


if __name__ == "__main__":
    app.run(debug=True)
