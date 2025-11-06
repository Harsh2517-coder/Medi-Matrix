# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from db_config import get_db_connection

auth_bp = Blueprint('auth', __name__)

# This User class is used by Flask-Login to manage the user session
class User:
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role
        self.is_active = True
        self.is_authenticated = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_from_form = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM Users WHERE Username = %s", (username,))
        user_data = cursor.fetchone()
        
        # Plain text password comparison (insecure)
        if user_data and user_data['Password'] == password_from_form:
            user = User(id=user_data['UserID'], username=user_data['Username'], role=user_data['Role'])
            login_user(user)
            flash('Logged in successfully!', 'success')
            
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'doctor':
                return redirect(url_for('doctor.dashboard'))
            elif user.role == 'patient':
                return redirect(url_for('patient.dashboard'))
            elif user.role == 'accountant':
                return redirect(url_for('accounts.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            
        cursor.close()
        conn.close()

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = get_db_connection()
        if conn is None:
            flash('Database connection failed. Please try again later.', 'danger')
            return redirect(url_for('auth.register'))
        
        cursor = conn.cursor(dictionary=True)
        # Common fields from the form
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        contact = request.form['contact_number']

        # Check if username already exists
        cursor.execute("SELECT * FROM Users WHERE Username = %s", (username,))
        if cursor.fetchone():
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('auth.register'))

        # 1. Create the main User account
        cursor.execute(
            "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)",
            (username, password, role)
        )
        user_id = cursor.lastrowid # Get the ID of the newly created user

        # 2. Create the specific profile based on the selected role
        try:
            if role == 'patient':
                address = request.form['address']
                dob = request.form['dob']
                gender = request.form['gender']
                cursor.execute(
                    "INSERT INTO Patients (UserID, FirstName, LastName, DateOfBirth, Gender, ContactNumber, Address) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (user_id, first_name, last_name, dob, gender, contact, address)
                )
            elif role == 'doctor':
                spec_id = request.form['specialization_id']
                hire_date = request.form['hire_date']
                cursor.execute(
                    "INSERT INTO Doctors (UserID, FirstName, LastName, SpecializationID, ContactNumber, HireDate) VALUES (%s, %s, %s, %s, %s, %s)",
                    (user_id, first_name, last_name, spec_id, contact, hire_date)
                )
            elif role in ['admin', 'accountant']:
                position = request.form['position']
                hire_date = request.form['hire_date']
                cursor.execute(
                    "INSERT INTO StaffProfiles (UserID, FirstName, LastName, Position, HireDate) VALUES (%s, %s, %s, %s, %s)",
                    (user_id, first_name, last_name, position, hire_date)
                )
            
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            conn.rollback() # Undo changes if an error occurs
            flash(f'An error occurred: {e}', 'danger')
        
        finally:
            cursor.close()
            conn.close()

    # For a GET request, fetch specializations for the doctor form dropdown
    conn = get_db_connection()
    specializations = []
    
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Specializations ORDER BY SpecializationName")
            specializations = cursor.fetchall() or []
            cursor.close()
        except Exception as e:
            print(f"Error fetching specializations: {e}")
            specializations = []
        finally:
            if conn:
                conn.close()
    
    return render_template('register.html', specializations=specializations)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    # No flash message - user is just redirected to login
    return redirect(url_for('auth.login'))