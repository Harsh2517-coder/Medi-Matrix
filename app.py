# app.py
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from db_config import get_db_connection

# Import blueprints
from routes.auth import auth_bp, User
from routes.patient import patient_bp
from routes.doctor import doctor_bp
from routes.accounts import accounts_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_very_secret_key_for_your_project' # Change this!

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT UserID, Username, Role FROM Users WHERE UserID = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    if user_data:
        return User(id=user_data['UserID'], username=user_data['Username'], role=user_data['Role'])
    return None

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(accounts_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def index():
    if current_user.is_authenticated:
        # Redirect to the respective dashboard
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'doctor':
            return redirect(url_for('doctor.dashboard'))
        elif current_user.role == 'patient':
            return redirect(url_for('patient.dashboard'))
        elif current_user.role == 'accountant':
            return redirect(url_for('accounts.dashboard'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)