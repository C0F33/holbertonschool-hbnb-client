from flask import Flask, render_template
from db import db
import os
from flask_jwt_extended import JWTManager
from api.user_manager import user_manager_blueprint
from api.country_city_manager import country_city_manager_blueprint
from api.amenity_manager import amenity_blueprint
from api.place_manager import place_manager_blueprint
from api.review_manager import review_manager_blueprint
from flask_migrate import Migrate

app = Flask(__name__, template_folder='../base_files',static_folder='../base_files')

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    JWT_SECRET_KEY = 'super-secret'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


environment_config = DevelopmentConfig if os.environ.get(
    'ENV') == 'development' else ProductionConfig
app.config.from_object(environment_config)

db.init_app(app)
jwt = JWTManager(app)


@app.route('/')
def home():
    return render_template('index.html')



app.register_blueprint(user_manager_blueprint)
app.register_blueprint(country_city_manager_blueprint)
app.register_blueprint(amenity_blueprint)
app.register_blueprint(place_manager_blueprint)
app.register_blueprint(review_manager_blueprint)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)