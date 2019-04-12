import os
from os.path import join, realpath, dirname
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

HTML_FOLDER = join(dirname(realpath(__file__)), 'html/')
BACKGROUND_FOLDER = join(dirname(realpath(__file__)), 'backgrounds/')
LOGOS_FOLDER = join(dirname(realpath(__file__)), 'logos/')
VIDEOS_FOLDER = join(dirname(realpath(__file__)), 'videos/')
SONGS_FOLDER = join(dirname(realpath(__file__)), 'songs/')
ALLOWED_EXTENSIONS = ('txt', "mp3", 'png', 'jpg', 'jpeg', 'gif', 'mp4')

app = Flask(__name__, static_url_path='/html')
app.config['HTML_FOLDER'] = HTML_FOLDER
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
                return redirect(url_for("uploaded_file"))
            else:
                return send_from_directory(app.config['HTML_FOLDER'], 'index.html')

    elif request.method == 'GET':
        return send_from_directory(HTML_FOLDER, 'index.html')


@app.route('/download', methods=['GET', 'POST'])
def download_file():
    return send_from_directory(app.config['BACKGROUNDS'], "01.mp4")

@app.route('/uploaded', methods=['GET'])
def uploaded_file():
    return '''
    <html>
    <head></head>
    <body>
    <title style='display:block;'>File uploaded</title></body>
    </html>
    '''


if __name__ == '__main__':
    app.run()
