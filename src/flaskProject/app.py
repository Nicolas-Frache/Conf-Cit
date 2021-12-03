from flask import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("pages/home.html")


if __name__ == '__main__':
    # Extension au moteur de template qui permet de passer des paramètres dans un include
    app.jinja_env.add_extension('jinja2.ext.with')
    app.run()
