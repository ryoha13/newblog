from ..main import main


@main.route('/')
def index():
    return 'index page'
