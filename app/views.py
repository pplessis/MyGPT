# Import the Flask class for Python web development
from flask import render_template, redirect, url_for, session, request, flash
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime as DT

from app                    import app
from .src                   import apiGpt as GPT
from .libs.src.utils        import Print

#SEE: https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html


#@app.route('/template/master.html')
#def base():
#    return render_template('master.html')

#@app.route('/user/<name>')
#def user(name:str):
#    return render_template('master.html' , name=name )

#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    if request.method == 'POST':
#        session['username'] = request.form['username']
#        session['name'] = session['username'].capitalize()
#        return redirect(url_for('index'))
#    return '''
#        <form method="post">
#            <p><input type=text name=username>
#            <p><input type=submit value=Login>
#        </form>
#    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('name', None)

    return redirect(url_for('index'))



##################

# App main route + generic routing
#@app.route('/', defaults={'path': 'index.html'})
#@app.route('/<path>')

@app.route('/')
def index():
     # Inject a simple flask message
    flash('[Flash message] current page: ') # + path)

    template = 'master.html'
    username = None
    name = None

    if 'username' in session:
        username = session['username']
    if 'name' in session:
        name = session['name']

    return render_template(template , session=username, name=name), 200

@app.route('/chat', methods=['POST'])
def chat():
    date =  DT.now().strftime('%Y-%m-%d %H:%M:%S')
    response = None
    # Manage input
    if (request.method == 'POST' and request.is_json and request.json != None):
        message = request.json.get('message', '')

    Print.log(f'Message POST: {message}' , 5)

    # Launch the chat with GPT
    myGPT = GPT.ApiGPT()
    #myGPT.api_url = 'http://walfred.local:11434/api/generate'
    #myGPT.api_url = 'http://127.0.0.1:11434/api/generate'
    #myGPT.api_url = 'http://10.0.0.222:11434/api/generate'
    myGPT.api_url = 'http://192.168.1.40:11434/api/generate'

    myGPT.model = "llama3.2"

    myGPT.temperature = 1
    myGPT.max_tokens = 10000
    #myGPT.promptTemplate = Io.openTxtFileStr('./', 'promptTemplate.txt')

    values = {'$REQUEST$' : message}

    response = myGPT.GetResponse(values, '$REQUEST$')


    Print.log (f'Message RESPONSE: {response}' , 5)


    #Manage output
    if response != None and len(response) > 0:
        return {'status': 'success', 'time': date, 'message': response}, 200

    return {'status': 'error', 'message': 'No message provided'}, 400

