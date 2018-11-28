import connexion
from people import verify_password
from people import identity

def create_app():
    # UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
    # Create the application instance
    app = connexion.FlaskApp(__name__, specification_dir='./', template_folder='templates')
    app.add_api('swagger.yml')
    app.app.config['SECRET_KEY'] = 'super-secret'

    from people import JWT
    jwt = JWT(app.app, verify_password, identity)

    return app
