from unittest import result
import cv2
import os
from PIL import Image
from numpy import asarray
from flask import Flask, render_template, request, Response, redirect, session, url_for, jsonify
from werkzeug.utils import secure_filename
import ktrain
from storage import Storage

model = ktrain.load_predictor('model')
user = Storage()

app = Flask(__name__) 
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = 'static/'
app.secret_key = 'AStupidConsistencyIsHobglobinOfLittleMind'

def generate_frames():
    camera=cv2.VideoCapture(0)
    while True:
        success,frame=camera.read()
        if not success:
            break 
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/reg')
def home():
    return render_template("signup.html")

@app.route('/register', methods=['POST'])
def register():
    """User registration"""
    if request.method ==  'POST':
        res = dict(request.form)
        result = user.new_user([res['sname'], res['fname'], res['email'], res['pnumber'], res['password']])
        if result:
            user.save()
            session['id'] = result.get('id')
            session['email'] = result.get('email')
            session['name'] = f"{result.get('sname')} {result.get('fname')}"
            return redirect(url_for('choose', message=f"Welcome Back {session.get('name')}!"))
    return redirect(url_for('home'))

@app.route('/login')
def login():
    """The login file"""
    message = request.args.get('message', '')
    if message is not None:
        message  = {'type': 'err-mes', 'class': 'content', 'text': message}
    return render_template("login.html", message=message)

@app.route('/sign', methods=['POST'])
def signin():
    """The login implementation endpoint"""
    if request.method ==  'POST':
        res = dict(request.form)
        result = user.get_user(res['email'], res['password'])
        if result:
            session['id'] = result.get('id')
            session['email'] = result.get('email')
            session['name'] = f"{result.get('sname').upper()} {result.get('fname').upper()}"
            return redirect(url_for('choose', message=f"Welcome Back {session.get('name')}!"))
    return redirect(url_for('login', message="Your email or password is not correct!"))

@app.route("/choose")
def choose():
    """choose between upload and take pics"""
    if not user.active:
        return redirect(url_for('login', message="Please Log in!"))
    message = request.args.get('message', '')
    message  = {'type': 'success-mes', 'class': 'content', 'text': message}
    return render_template('chose.html', message=message)

@app.route('/capture')
def capture():
    """capture file"""
    if not user.active:
        return redirect(url_for('login', message="Please Log in!"))
    return render_template("result.html")

@app.route("/uploader" , methods=['POST'])
def uploader():
    if user.active:  
        if request.method=='POST':
            f = request.files['file1']
            extension = f.filename.split('.')[1]
            f.filename = session.get('id') + '.' + extension
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            result = round(model.predict_filename(f"static/{f.filename}")[0])
            pic1 = os.path.join(app.config['UPLOAD_FOLDER'], f'{f.filename}')
            user.add_image_url(session.get('id'), pic1)
            user.save()
            return render_template("final.html", predicted_digit=result, input_image=f.filename)
    return redirect(url_for('login', message="Please Log in!"))

@app.route("/uploaded" , methods=['POST'])
def uploaded():
    if user.active:  
        if request.method=='POST':
            f = request.files['file1']
            extension = f.filename.split('.')[1]
            f.filename = session.get('id') + '.' + extension
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            result = round(model.predict_filename(f"static/{f.filename}")[0])
            pic1 = os.path.join(app.config['UPLOAD_FOLDER'], f'{f.filename}')
            user.add_image_url(session.get('id'), pic1)
            user.save()
            result_url = url_for('result', predicted_digit=result, input_image=f.filename, _external=True)
            response_data = {'redirect_url': result_url}
            return jsonify(response_data)
    return redirect(url_for('login', message="Please Log in!"))

@app.route("/result")
def result():
    predicted_digit = request.args.get('predicted_digit')
    input_image = request.args.get('input_image')
    return render_template("final.html", predicted_digit=predicted_digit, input_image=input_image)

@app.route('/logout')
def logout():
    """logout"""
    if user.active:
        del session['id']
        del session['name']
        del session['email']
        user.logout()
    return redirect(url_for('login', message="You can login back!"))




@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True) 