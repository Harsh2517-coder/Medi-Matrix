# routes/patient.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from db_config import get_db_connection
from datetime import datetime, date, timedelta # New imports

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

@patient_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'patient':
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT PatientID FROM Patients WHERE UserID = %s", (current_user.id,))
    patient = cursor.fetchone()
    if not patient:
        flash("Patient profile not found!", "danger")
        return redirect(url_for('auth.logout'))

    query = """
    SELECT a.AppointmentDateTime, d.FirstName, d.LastName, s.SpecializationName, a.Status, a.Diagnosis
    FROM Appointments a
    JOIN Doctors d ON a.DoctorID = d.DoctorID
    JOIN Specializations s ON d.SpecializationID = s.SpecializationID
    WHERE a.PatientID = %s
    ORDER BY a.AppointmentDateTime DESC;
    """
    cursor.execute(query, (patient['PatientID'],))
    appointments = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('patient/dashboard.html', appointments=appointments)

@patient_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book_appointment():
    if current_user.role != 'patient':
        return redirect(url_for('auth.login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        app_date_str = request.form['appointment_date']
        
        # --- ADDED: Backend validation to check the date ---
        appointment_date_obj = datetime.strptime(app_date_str, '%Y-%m-%d').date()
        if appointment_date_obj <= date.today():
            flash('Appointment date must be in the future.', 'danger')
            return redirect(url_for('patient.book_appointment'))
        # --- END OF VALIDATION ---

        doc_id = request.form['doctor']
        app_time = request.form['appointment_time']
        reason = request.form['reason']

        cursor.execute("SELECT PatientID FROM Patients WHERE UserID = %s", (current_user.id,))
        patient = cursor.fetchone()
        
        app_datetime = f"{app_date_str} {app_time}"

        insert_query = """
        INSERT INTO Appointments (PatientID, DoctorID, AppointmentDateTime, Reason, Status)
        VALUES (%s, %s, %s, %s, 'Pending')
        """
        cursor.execute(insert_query, (patient['PatientID'], doc_id, app_datetime, reason))
        conn.commit()
        
        flash('Appointment requested successfully! You will be notified upon confirmation.', 'success')
        return redirect(url_for('patient.dashboard'))

    # For GET request, fetch data for dropdowns
    cursor.execute("SELECT * FROM Specializations")
    specializations = cursor.fetchall()
    
    cursor.execute("""
    SELECT d.DoctorID, d.FirstName, d.LastName, s.SpecializationName, d.SpecializationID
    FROM Doctors d JOIN Specializations s ON d.SpecializationID = s.SpecializationID
    """)
    doctors = cursor.fetchall()

    cursor.close()
    conn.close()

    # --- ADDED: Calculate the minimum selectable date (tomorrow) ---
    min_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    return render_template('patient/book_appointment.html', 
                           specializations=specializations, 
                           doctors=doctors,
                           min_date=min_date) # <-- Pass min_date to the template