import logging
import os
import shutil
from flask import (Flask, render_template, request, url_for,
                   redirect, flash)
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename


upload_path = "static/img"
backup_path = "static/img_backup"
allowed_extensions = ['png', 'jpg', 'jpeg', 'gif']


app = Flask(__name__)
app.secret_key = "ja;kdsjfadnf,manvklsueejrlweuroqueoup34iou2cnz.,"
app.config['upload_path'] = upload_path
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


class LoginForm(Form):
    username = StringField('Username',
                           validators=[
                               DataRequired(),
                           ])
    password = PasswordField("Password",
                             validators=[
                                 DataRequired(),
                             ])


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'mbrumbley' and form.password.data == 'boots':
            return redirect(url_for('index'))
        else:
            flash("Wrong username or password")
    return render_template('login.html', form=form)

@app.route('/main')
def index():
    images = []
    for filename in os.listdir(upload_path):
        print(filename)
        images.append(filename)
    return render_template('index.html', images=images)


@app.route('/add_image', methods=('GET', 'POST'))
def add_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            # flash("No file attached")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No file attached!")
            return redirect(request.url)
        if allowed_filename(file.filename) == False:
            flash("Can't upload that type of file!")
            flash("File must be a png, jpg, or gif")
            return redirect(request.url)
        if file and allowed_filename(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['upload_path'], filename))
            return redirect(url_for('index'))
    return render_template('add_image.html')


@app.route('/delete_image', methods=('GET', 'POST'))
def delete_image():
    images = []
    for filename in os.listdir('static/img'):
        print(filename)
        images.append(filename)
    flash("Click an image to delete it")
    return render_template('delete_image.html', images=images)


@app.route('/delete_image/<image_url>', methods=('GET', 'POST'))
def delete(image_url):
    images = []
    for filename in os.listdir('static/img'):
        print(filename)
        images.append(filename)
    if image_url in images:
        os.remove(os.path.join(app.config['upload_path'], image_url))
    return redirect(url_for('delete_image'))


@app.route('/reset', methods=('GET', 'POST'))
def reset():
    old_images = []
    new_images = []
    for filename in os.listdir(upload_path):
        old_images.append(filename)
    for old in old_images:
        os.remove(os.path.join(app.config['upload_path'], old))
    for file in os.listdir(backup_path):
        shutil.copy(backup_path + '/' + file, upload_path)
    for filename in os.listdir(upload_path):
        new_images.append(filename)
    return render_template('index.html', images=new_images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
