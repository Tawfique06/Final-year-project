from unittest import result
import cv2
import os
from PIL import Image
from numpy import asarray
from flask import Flask, render_template, request, Response, redirect
from werkzeug.utils import secure_filename
import ktrain
from storage import Storage

model = ktrain.load_predictor('model')
user = Storage()

app = Flask(__name__) 
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = 'static/'

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
def home():
    return render_template("signup.html")

@app.route('/sub', methods=['POST'])
def register():
    """User registration"""
    if request.method ==  'POST':
        res = dict(request.form)
        result = user.new_user([res['sname'], res['fname'], res['email'], res['pnumber'], res['password']])
        if result:
            return redirect('login')
    return redirect('home')

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/webcam', methods=['GET', 'POST'])
def webcam():
    return render_template("webcam.html")

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam_image_predict', methods=['GET', 'POST'])
def webcam_image_predict():
    result = round(model.predict_filename("static/webcam_image.jpg")[0])
    return str(result)

@app.route('/capture_and_show_pic', methods=['GET', 'POST'])
def capture_and_show_pic():
    camera=cv2.VideoCapture(0)
    while True:
        success,frame=camera.read()
        if not success:
            break
        else:
            cv2.imwrite("static/webcam_image.jpg", frame)
            break
    return "Success"

@app.route("/uploader" , methods=['GET', 'POST'])
def uploader():    
    if request.method=='POST':
        f = request.files['file1']
        f.filename = "image.jpg"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        result = round(model.predict_filename("static/image.jpg")[0])
        pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg')
        return render_template("uploaded.html", predicted_digit=result, input_image=pic1) 

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True) 