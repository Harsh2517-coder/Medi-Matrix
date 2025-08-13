# routes/admin.py
from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from db_config import get_db_connection

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def check_is_admin():
    if current_user.role != 'admin':
        abort(403)

@admin_bp.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Dashboard Metrics
    cursor.execute("SELECT COUNT(*) AS count FROM Doctors")
    doctor_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) AS count FROM Appointments WHERE Status = 'Pending'")
    pending_appointments = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) AS count FROM Patients")
    patient_count = cursor.fetchone()['count']

    # Note: Bed count is a placeholder as it's not in the DB schema
    beds_available = 50 
    
    cursor.close()
    conn.close()
    
    return render_template('admin/dashboard.html', 
                           doctor_count=doctor_count,
                           pending_appointments=pending_appointments,
                           patient_count=patient_count,
                           beds_available=beds_available)

@admin_bp.route('/appointments')
def appointment_requests():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT a.AppointmentID, a.AppointmentDateTime, a.Reason, p.FirstName AS pFirstName, p.LastName AS pLastName,
           d.FirstName AS dFirstName, d.LastName AS dLastName
    FROM Appointments a
    JOIN Patients p ON a.PatientID = p.PatientID
    JOIN Doctors d ON a.DoctorID = d.DoctorID
    WHERE a.Status = 'Pending'
    ORDER BY a.AppointmentDateTime ASC;
    """
    cursor.execute(query)
    requests = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('admin/appointment_requests.html', requests=requests)

@admin_bp.route('/appointment/approve/<int:appointment_id>')
def approve_appointment(appointment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Appointments SET Status = 'Confirmed' WHERE AppointmentID = %s", (appointment_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f"Appointment #{appointment_id} has been confirmed.", 'success')
    return redirect(url_for('admin.appointment_requests'))

@admin_bp.route('/appointment/decline/<int:appointment_id>')
def decline_appointment(appointment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Appointments SET Status = 'Cancelled' WHERE AppointmentID = %s", (appointment_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f"Appointment #{appointment_id} has been declined.", 'warning')
    return redirect(url_for('admin.appointment_requests'))

@admin_bp.route('/staff')
def staff_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get Doctors
    cursor.execute("""
    SELECT d.FirstName, d.LastName, s.SpecializationName, d.ContactNumber, d.HireDate
    FROM Doctors d JOIN Specializations s ON d.SpecializationID = s.SpecializationID
    """)
    doctors = cursor.fetchall()

    # Get Admins and Accountants
    cursor.execute("""
    SELECT sp.FirstName, sp.LastName, sp.Position, u.Username
    FROM StaffProfiles sp JOIN Users u ON sp.UserID = u.UserID
    WHERE u.Role IN ('admin', 'accountant')
    """)
    other_staff = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('admin/staff_list.html', doctors=doctors, other_staff=other_staff)