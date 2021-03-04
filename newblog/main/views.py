from flask import render_template, send_from_directory, current_app
from ..main import main


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)