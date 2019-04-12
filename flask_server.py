import os
from os.path import join, realpath, dirname
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from image_scaler import *
from main import one_on_each_other


DIR_PATH = dirname(realpath(__file__))
DOCUMENTS = join(DIR_PATH, 'documents/')
STATIC_FOLDER = join(DOCUMENTS, 'static/')
BACKGROUND_FOLDER = join(DOCUMENTS, 'backgrounds/')
LOGOS_FOLDER = join(DOCUMENTS, 'logos/')
VIDEOS_FOLDER = join(DOCUMENTS, 'videos/')
SONGS_FOLDER = join(DOCUMENTS, 'songs/')
ALLOWED_EXTENSIONS = ('txt', "mp3", 'png', 'jpg', 'jpeg', 'gif', 'mp4')

app = Flask(__name__, static_url_path=STATIC_FOLDER)
app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.config['BACKGROUNDS'] = BACKGROUND_FOLDER
app.config['LOGOS'] = LOGOS_FOLDER
app.config['VIDEOS'] = VIDEOS_FOLDER
app.config['SONGS'] = SONGS_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if not request.files:
            flash('No file part')
            return redirect(request.url)

        for check_name in ("backgrounds", "logos", "songs", "videos"):
            file_list = request.files.getlist(check_name)
            if file_list:
                for file in file_list:
                    if file.filename == '':
                        flash('No selected file')
                        return redirect(request.url)
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config[check_name.upper()], filename))
            else:
                continue
            scale_images(app.config['BACKGROUNDS'])

            return "File uploaded"
    elif request.method == 'GET':
        return render_template('index.html')


@app.route('/one_on_each_other', methods=['GET'])
def test_movie():
    clip = one_on_each_other([os.path.join(app.config['BACKGROUNDS'], '01.jpg'), os.path.join(app.config['BACKGROUNDS'], '02.jpg'), os.path.join(app.config['BACKGROUNDS'], '03.jpg')])
    clip.write_videofile("final.mp4", fps=25)
    return send_from_directory(dirname(realpath(__file__)), "final.mp4")


if __name__ == '__main__':
    app.run()
