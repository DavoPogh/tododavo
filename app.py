from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

# Initializing extensions
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Redirect to login if not authenticated

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.db')
    app.config['SECRET_KEY'] = 'secret'

    from models import db
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from auth import auth_bp
        from tasks import tasks_bp
        from home import home_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(tasks_bp)
        app.register_blueprint(home_bp)

        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

