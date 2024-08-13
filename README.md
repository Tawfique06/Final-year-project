# Final-year-project: Automatic Facial Age Estimator Web App
Web Application for Automatic Facial Age Estimation of Black Persons(Deep learning approach)

## Tools used
- Programming language and frameworks: Python, Tensorflow, Ktrain, Flask, Git-Bash
- Model training and evaluation: Google colab, Vs code
- WebApp: HTML, CSS, JSON, Python, Flask
- Dataset: BlackFaces
- Offline testing: Vscode terminal and Chrome browser
- Online testing: Digital Ocean

## How To Use this Web app
1. You clone this repo or download the code as zip file.
   - Extract the zip file on your PC.
   - The model size is above Github file size limit. Download the model from from here. ![model](https://drive.google.com/drive/folders/1KlAGHDwihZIUSw7oi5FGVXxtaH7_a0qq?usp=sharing) and place the model binary files in the `model` folder
   - Open a Terminal(Cmd/Bash) to run the App

2. It's recommended that a virtual environment is used to install the app packages. [virtual env documentation](https://docs.python.org/3/library/venv.html)
   - For Gitbash: Type the code `python -m venv afae_venv` to setup a virtual environment. And
   - Activate the virtual env. with `source venv /afae_venv`

3. Install the requirements.txt file to automatically download and setup the app dependencies(packages).
   - Use the command `pip install -r requirements.txt` to set up the app on your PC

4. Launch the WebApp(Offline Setup)
   - Use `python app.py` or `flask --app run app.py`

5. The terminal should display a default IP address to run WebApp in your browser.
   - Ensure the computer is connected to the internet so that the Web UI bootstrap components can be loaded for a beautiful interface.
   - Proceed to test the App

6. Register as new user or loging with initial credentials after your first login.
   - You try the Automatic Facial age estimation as many time as you want.
   - Ensure the system can detect your face(proper room lightning)

7. For live testing and Demo anywhere.
   -The WebApp is deployed on Heroku and it's available 24/7 online. ![check it](https://digitalocean.com). App not available

   *PS: Incase of any bug or misinformation, kindly reach out to the developer of the WebApp via email*
   [Email us](htaofeek95@gmail.com)

(c) 2024. All rights reserved.
