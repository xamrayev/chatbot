from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import g4f
from markdown import markdown
app = Flask(__name__)
app.config['SECRET_KEY'] = 'salom'
login_manager = LoginManager()
login_manager.init_app(app)

users = {
    'user1': {'username': 'user1', 'password': 'password1'},
    'user2': {'username': 'user2', 'password': 'password2'},
}

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return None
    user = User()
    user.id = username
    return user

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('welcome'))

    return render_template('login2.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            users[username] = {'username': username, 'password': password}
            return redirect(url_for('login'))

    return render_template('register2.html')


@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome2.html', current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/protected')
@login_required
def protected():
    return f"Welcome to the protected page, {current_user.id}!"


def chatbot2(question):
   promt2=question
   if promt2 =="":
    response = '''
    # It is a Chatbot!
    This is a **GPT** based bot.
    '''
   else:
       response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": promt2}],
        )
    
   return response

@app.route('/image')
def image():
    return ('assets')

@app.route('/chatbot', methods=['POST'])
@login_required
def chatbot():
    question = request.form['zapros']
    response = chatbot2(question)
    while response=="<PHIND_BACKEND_ERROR>Invalid request body</PHIND_BACKEND_ERROR>":
        response = chatbot2(question)
    question = ""

    html_string = markdown(response)

    return render_template('welcome2.html', string=html_string)

if __name__ == '__main__':
    app.run(debug=True)