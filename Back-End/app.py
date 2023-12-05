from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong, random value

# Dummy user data (replace this with a database in a real application)
users = {'username': 'password','keerthi':'2003','suji':'2003','raj':'hi','ravi':'ravi','username1':'password1','username2':'password2','vikram':'vikky'}

# URL data structure to store generated URLs and their expiration times
url_data = {}


def generate_url():
    unique_id = str(uuid.uuid4())
    expiration_time = datetime.now() + timedelta(hours=48)
    url_data[unique_id] = expiration_time
    return unique_id


def is_url_valid(url_id):
    if url_id in url_data:
        current_time = datetime.now()
        expiration_time = url_data[url_id]
        return current_time < expiration_time
    return False


@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/generate_url')
def generate_and_display_url():
    if 'username' in session:
        url_id = generate_url()
        return render_template('generate_url.html', url_id=url_id)
    return redirect(url_for('login'))


@app.route('/<url_id>')
def view_url(url_id):
    if is_url_valid(url_id):
        return render_template('view_url.html', url_id=url_id)
    return 'URL is not valid or has expired.'


if __name__ == '__main__':
    app.run(debug=True)
