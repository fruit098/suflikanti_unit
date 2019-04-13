import os
from os.path import join, realpath, dirname
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, send_file
from werkzeug.utils import secure_filename
from image_scaler import *
from random import choice
from transition import *

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
    if request.method == 'POST':
        options = request.form.to_dict(flat=False)
        options = {key: options[key][0] for key in options.keys()}
        clip_path = movie_creation(**options)
        return send_file(join(dirname(realpath(__file__)), clip_path),as_attachment=True)


def movie_creation(duration=3, fast=False, intro=False, outro=False, platform="IG"):
    count_of_pic = int(duration)
    intro = False if intro == 'False' else True
    outro = False if intro == 'False' else True

    fast_multi_trans = multifast
    slow_multi_trans = multislow

    fast_one_trans = onefast
    slow_one_trans = oneslow

    platform_to_choose = "instagram_" if platform == "IG" else "facebook_"
    scale_images(BACKGROUND_FOLDER)

    all_files = os.listdir(BACKGROUND_FOLDER)
    chosen_pics = validate_pics_and_choose_subset(all_files, platform_to_choose, count_of_pic)

    #function make intro
    clip = None
    count_of_pic = int(count_of_pic)
    if count_of_pic > 2:
        if fast:
            chosen_trans = choice(fast_multi_trans)
        else:
            chosen_trans = choice(slow_multi_trans)
    else:
        if fast:
            chosen_trans = choice(fast_one_trans)
        else:
            chosen_trans = choice(slow_one_trans)

    pics_with_path = [join(BACKGROUND_FOLDER, pic) for pic in chosen_pics]
    clip = chosen_trans(pics_with_path[0] if count_of_pic == 1 else pics_with_path)

    if outro:
        #add outro
        pass
    path = "final.mp4"
    clip.write_videofile(path, fps=25)
    return path


def validate_pics_and_choose_subset(files, platform, count_of_pics):
    valid_pics = []
    chosen_pics = []
    for pic in files:
        if platform in pic and pic[0] != ".":
            valid_pics.append(pic)

    for i in range(count_of_pics):
        chosen_pic = (choice(valid_pics))
        chosen_pics.append(chosen_pic)
        valid_pics.pop(valid_pics.index(chosen_pic))
        if not valid_pics:
            return chosen_pics

    return chosen_pics


if __name__ == '__main__':
    app.run()
