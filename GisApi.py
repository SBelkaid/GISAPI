from flask import render_template
import connexion, os

# Create the application instance
app = connexion.FlaskApp(__name__, specification_dir='./', template_folder='templates')
app.add_api('swagger.yml')
DATABASE_URI = '/tmp/db.sqlite'
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')


# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
