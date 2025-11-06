# routes/doctor.py
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from db_config import get_db_connection

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')

# A helper function to get the DoctorID from the current user's UserID
def get_doctor_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT DoctorID FROM Doctors WHERE UserID = %s", (user_id,))
    doctor = cursor.fetchone()
    cursor.close()
    conn.close()
    return doctor['DoctorID'] if doctor else None

@doctor_bp.before_request
@login_required
def check_is_doctor():
    if current_user.role != 'doctor':
        abort(403) # Forbidden

@doctor_bp.route('/dashboard')
def dashboard():
    doctor_id = get_doctor_id(current_user.id)
    if not doctor_id:
        return "Doctor profile not found.", 404

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get list of all appointments for the logged-in doctor
    query = """
    SELECT a.AppointmentDateTime, a.Status, a.Reason, p.FirstName, p.LastName
    FROM Appointments a
    JOIN Patients p ON a.PatientID = p.PatientID
    WHERE a.DoctorID = %s
    ORDER BY a.AppointmentDateTime DESC;
    """
    cursor.execute(query, (doctor_id,))
    appointments = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('doctor/dashboard.html', appointments=appointments)

@doctor_bp.route('/patients')
def patient_list():
    doctor_id = get_doctor_id(current_user.id)
    if not doctor_id:
        return "Doctor profile not found.", 404

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get a unique list of all patients treated by this doctor
    query = """
    SELECT DISTINCT p.PatientID, p.FirstName, p.LastName, p.ContactNumber, p.DateOfBirth
    FROM Patients p
    JOIN Appointments a ON p.PatientID = a.PatientID
    WHERE a.DoctorID = %s;
    """
    cursor.execute(query, (doctor_id,))
    patients = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('doctor/patient_list.html', patients=patients)

@doctor_bp.route('/salary')
def salary_history():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get salary history for the logged-in user
    query = "SELECT Amount, PaymentDate, Notes FROM Salaries WHERE UserID = %s ORDER BY PaymentDate DESC"
    cursor.execute(query, (current_user.id,))
    salaries = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('doctor/salary_history.html', salaries=salaries)