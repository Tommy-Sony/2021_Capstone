from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db =SQLAlchemy()
migrate= Migrate()

app = Flask(__name__)


@app.route('/')
def basic():
    return render_template("main.html")

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/config')
def config():
    return render_template("configuration.html")


#if __name__=='__main__':
#    app.run(debug=True)


def create_app():
    #app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    return app
