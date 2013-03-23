import flask.ext.restless
import flask.ext.sqlalchemy
from flask import Flask, render_template


app = Flask(__name__)


# Create the Flask-SQLAlchemy object and an SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = flask.ext.sqlalchemy.SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=False)
    is_completed = db.Column(db.Boolean)

    # When we create a new Todo it should be incomplete and have a title
    def __init__(self, title, is_completed=False):
        self.title = title
        self.is_completed = is_completed

# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
restless_manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)


def ember_formatter(results):
    return {'todos': results['objects']} if 'page' in results else results


def pre_ember_formatter(results):
    return results['todo']


def pre_patch_ember_formatter(instid, results):
    return results['todo']

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
restless_manager.create_api(
    Todo,
    methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'],
    url_prefix='/api',
    collection_name='todos',
    results_per_page=-1,
    postprocessors={
        'GET_MANY': [ember_formatter]
    },
    preprocessors={
        'POST': [pre_ember_formatter],
        'PUT_SINGLE': [pre_patch_ember_formatter]
    }
)

app.debug = True


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
