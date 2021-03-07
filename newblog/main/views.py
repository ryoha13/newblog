from flask import render_template, send_from_directory, current_app, request, redirect, url_for, flash
from ..main import main
from ..models import Post


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLOG_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    return render_template('main/index.html', pagination=pagination, posts=posts)


@main.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)


@main.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('main/post.html', post=post)