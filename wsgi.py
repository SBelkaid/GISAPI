from factory import create_app
from flask import render_template

application = create_app()

@application.route('/home')
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')

if __name__ == "__main__":
    application.run(debug=True)
