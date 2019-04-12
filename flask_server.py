import os
from os.path import join, realpath, dirname
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from image_scaler import *
from main import one_on_each_other
from random import choice

DIR_PATH = dirname(realpath(__file__))
DOCUMENTS = join(DIR_PATH, 'documents')
STATIC_FOLDER = join(DIR_PATH, 'static')
TEMPLATES_FOLDER = join(DIR_PATH, 'templates')
BACKGROUND_FOLDER = join(DOCUMENTS, 'backgrounds')
LOGOS_FOLDER = join(DOCUMENTS, 'logos')
VIDEOS_FOLDER = join(DOCUMENTS, 'videos')
SONGS_FOLDER = join(DOCUMENTS, 'songs')
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


@app.route('/produce_video', methods=['GET', 'POST'])
def test_movie():
    pics_list = []
    for file in os.listdir(BACKGROUND_FOLDER):
        if file[0] != ".":
            pics_list.append(file)

    clip = one_on_each_other([join(BACKGROUND_FOLDER, choice(pics_list)) for _ in range(3)])
    clip.write_videofile("final.mp4", fps=25, codec="m")
    return send_from_directory(dirname(realpath(__file__)), "final.mp4")


def movie_creation(duration=3, fast=False, intro=False, outro=False, platform="IG"):
    fast_multi_trans = []
    slow_multi_trans = []

    fast_one_trans = []
    slow_one_trans = []

    platform_to_choose = "instagram_" if platform == "IG" else "facebook_"
    scale_images(BACKGROUND_FOLDER)

    all_files = os.listdir(BACKGROUND_FOLDER)
    chosen_pics = validate_pics_and_choose_subset(all_files, platform_to_choose, duration)

    #function make intro

    clip = None
    if duration > 2:
        if fast:
            chosen_trans = choice(fast_multi_trans)
        else:
            chosen_trans = choice(slow_multi_trans)
        clip = chosen_trans()
    else:
        if fast:
            chosen_trans = choice(fast_one_trans)
        else:
            chosen_trans = choice(slow_one_trans)

    clip = chosen_trans(chosen_pics)

    if outro:
        #add outro
        pass


def validate_pics_and_choose_subset(files, platform, duration):
    valid_pics = []
    chosen_pics = []
    for pic in files:
        if platform in pic and pic[0] != ".":
            valid_pics.append(pic)

    for _ in range(duration):
        chosen_pic = (choice(valid_pics))
        chosen_pics.append(chosen_pic)
        valid_pics.pop(chosen_pic)
        if not valid_pics:
            return chosen_pics

    return chosen_pics


if __name__ == '__main__':
    app.run()
