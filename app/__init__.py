from flask import Flask
from .database import db  # Mengimpor db dari database.py
from flask_login import LoginManager
from .models import User  # Pastikan untuk mengimpor model User

login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Rute login

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Memuat pengguna berdasarkan ID

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Pastikan ini sesuai dengan konfigurasi Anda
    
    db.init_app(app)  # Mengaitkan objek db dengan aplikasi
    login_manager.init_app(app)

    from . import routes  # Mengimpor rute
    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all()  # Buat database jika belum ada

    return app