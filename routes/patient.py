# routes/patient.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from db_config import get_db_connection
from datetime import datetime, date, timedelta

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

@patient_bp.route('/test')
def test_route():
    """Test route to verify routing works"""
    return "Patient routes are working! Book appointment route: /patient/book"

@patient_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'patient':
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    if not conn:
        flash("Database connection error. Please try again later.", "danger")
        return render_template('patient/dashboard.html', appointments=[])
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT PatientID FROM Patients WHERE UserID = %s", (current_user.id,))
        patient = cursor.fetchone()
        if not patient:
            flash("Patient profile not found!", "danger")
            cursor.close()
            conn.close()
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
    except Exception as e:
        flash(f"Error loading appointments: {str(e)}", "danger")
        appointments = []
    finally:
        cursor.close()
        conn.close()
    
    return render_template('patient/dashboard.html', appointments=appointments)

@patient_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book_appointment():
    """Book appointment route - always returns a page, never hangs"""
    print(f"[DEBUG] Book appointment route called - Method: {request.method}, User: {current_user.username if current_user.is_authenticated else 'Not authenticated'}")
    
    # Quick role check
    if current_user.role != 'patient':
        flash('Access denied. Please login as a patient.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Handle POST request
    if request.method == 'POST':
        print("[DEBUG] Handling POST request")
        return handle_appointment_submission()
    
    # Handle GET request - load the form (ALWAYS returns immediately, never hangs)
    print("[DEBUG] Handling GET request - loading form")
    try:
        result = load_appointment_form()
        print("[DEBUG] Form loaded successfully")
        return result
    except Exception as e:
        # Even if load_appointment_form fails, return a page
        print(f"[DEBUG] Critical error in book_appointment: {e}")
        import traceback
        traceback.print_exc()
        min_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        return render_template('patient/book_appointment.html', 
                               specializations=[], 
                               doctors=[],
                               min_date=min_date,
                               error_message=f'Error loading page: {str(e)}')

def handle_appointment_submission():
    """Handle appointment form submission"""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        if not conn:
            flash('Database connection error. Please try again later.', 'danger')
            return redirect(url_for('patient.book_appointment'))
            
        cursor = conn.cursor(dictionary=True)
        
        # Validate all required fields
        if 'appointment_date' not in request.form or not request.form['appointment_date']:
            flash('Please select an appointment date.', 'danger')
            return redirect(url_for('patient.book_appointment'))
        
        if 'doctor' not in request.form or not request.form['doctor']:
            flash('Please select a doctor.', 'danger')
            return redirect(url_for('patient.book_appointment'))
        
        if 'appointment_time' not in request.form or not request.form['appointment_time']:
            flash('Please select an appointment time.', 'danger')
            return redirect(url_for('patient.book_appointment'))
        
        if 'reason' not in request.form or not request.form['reason'].strip():
            flash('Please enter a reason for the visit.', 'danger')
            return redirect(url_for('patient.book_appointment'))

        app_date_str = request.form['appointment_date']
        doc_id = request.form['doctor']
        app_time = request.form['appointment_time']
        reason = request.form['reason'].strip()
        
        # Backend validation to check the date
        try:
            appointment_date_obj = datetime.strptime(app_date_str, '%Y-%m-%d').date()
            if appointment_date_obj <= date.today():
                flash('Appointment date must be in the future.', 'danger')
                return redirect(url_for('patient.book_appointment'))
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('patient.book_appointment'))

        # Verify doctor exists
        cursor.execute("SELECT DoctorID FROM Doctors WHERE DoctorID = %s", (doc_id,))
        doctor = cursor.fetchone()
        if not doctor:
            flash('Selected doctor does not exist.', 'danger')
            return redirect(url_for('patient.book_appointment'))

        # Get patient ID
        cursor.execute("SELECT PatientID FROM Patients WHERE UserID = %s", (current_user.id,))
        patient = cursor.fetchone()
        
        if not patient:
            flash('Patient profile not found!', 'danger')
            return redirect(url_for('patient.dashboard'))
        
        # Combine date and time
        app_datetime = f"{app_date_str} {app_time}"

        # Insert appointment
        insert_query = """
        INSERT INTO Appointments (PatientID, DoctorID, AppointmentDateTime, Reason, Status)
        VALUES (%s, %s, %s, %s, 'Pending')
        """
        cursor.execute(insert_query, (patient['PatientID'], doc_id, app_datetime, reason))
        conn.commit()
        
        flash('Appointment requested successfully! You will be notified upon confirmation.', 'success')
        return redirect(url_for('patient.dashboard'))
        
    except KeyError as e:
        if conn:
            conn.rollback()
        flash(f'Missing required field: {str(e)}', 'danger')
        return redirect(url_for('patient.book_appointment'))
    except Exception as e:
        if conn:
            conn.rollback()
        flash(f'Error booking appointment: {str(e)}', 'danger')
        return redirect(url_for('patient.book_appointment'))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def load_appointment_form():
    """Load the appointment booking form - ALWAYS returns a page immediately, never hangs"""
    # Calculate minimum date first (no database needed) - do this IMMEDIATELY
    min_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Default values - set immediately
    specializations = []
    doctors = []
    error_message = None
    
    # Try to connect to database with quick timeout
    conn = None
    cursor = None
    
    try:
        # Quick connection attempt - don't wait long
        conn = get_db_connection()
        
        if conn is None:
            # Connection failed - return page immediately
            error_message = 'Database connection failed. Please check if MySQL is running and refresh the page.'
            return render_template('patient/book_appointment.html', 
                                   specializations=[], 
                                   doctors=[],
                                   min_date=min_date,
                                   error_message=error_message)
        
        # Connection successful - fetch data quickly
        cursor = conn.cursor(dictionary=True)
        
        # Fetch specializations - quick query
        try:
            cursor.execute("SELECT * FROM Specializations ORDER BY SpecializationName LIMIT 100")
            specializations = cursor.fetchall() or []
        except Exception as e:
            print(f"Error fetching specializations: {e}")
            specializations = []
            error_message = 'Could not load specializations.'
        
        # Fetch doctors - quick query
        try:
            cursor.execute("""
            SELECT d.DoctorID, d.FirstName, d.LastName, s.SpecializationName, d.SpecializationID
            FROM Doctors d 
            JOIN Specializations s ON d.SpecializationID = s.SpecializationID
            ORDER BY s.SpecializationName, d.LastName, d.FirstName
            LIMIT 200
            """)
            doctors = cursor.fetchall() or []
        except Exception as e:
            print(f"Error fetching doctors: {e}")
            doctors = []
            if not error_message:
                error_message = 'Could not load doctors.'
        
    except Exception as e:
        # Any error - return page immediately
        print(f"Error in load_appointment_form: {e}")
        error_message = f'Error: {str(e)}'
    finally:
        # Always close connections
        if cursor:
            try:
                cursor.close()
            except:
                pass
        if conn:
            try:
                conn.close()
            except:
                pass
    
    # ALWAYS return the template immediately - no matter what
    return render_template('patient/book_appointment.html', 
                           specializations=specializations, 
                           doctors=doctors,
                           min_date=min_date,
                           error_message=error_message)
