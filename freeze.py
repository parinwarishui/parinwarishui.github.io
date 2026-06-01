from flask_frozen import Freezer
from app import app, load_content, POSTS_DIR, PROJECTS_DIR

freezer = Freezer(app)
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True


@freezer.register_generator
def post():
    for p in load_content(POSTS_DIR):
        yield {'slug': p['slug']}


@freezer.register_generator
def project():
    for p in load_content(PROJECTS_DIR):
        yield {'slug': p['slug']}

if __name__ == '__main__':
    freezer.freeze()
    print('Successfully built to /build/')