# routes/accounts.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, Response
from flask_login import login_required, current_user
from db_config import get_db_connection
from weasyprint import HTML

accounts_bp = Blueprint('accounts', __name__, url_prefix='/accounts')

@accounts_bp.before_request
@login_required
def check_is_accountant():
    if current_user.role != 'accountant':
        abort(403)

@accounts_bp.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch all hospital expenses
    cursor.execute("SELECT * FROM Expenses ORDER BY ExpenseDate DESC")
    expenses = cursor.fetchall()
    
    # Fetch all salary records to display
    salary_query = """
    SELECT s.Amount, s.PaymentDate, s.Notes, u.Username, p.FirstName, p.LastName
    FROM Salaries s
    JOIN Users u ON s.UserID = u.UserID
    LEFT JOIN Patients p ON u.UserID = p.UserID
    ORDER BY s.PaymentDate DESC;
    """
    cursor.execute(salary_query)
    salaries = cursor.fetchall()

    # Fetch all invoices to display on the dashboard
    cursor.execute("""
        SELECT i.InvoiceID, i.TotalAmount, i.InvoiceDate, i.Status, p.FirstName, p.LastName
        FROM Invoices i JOIN Appointments a ON i.AppointmentID = a.AppointmentID
        JOIN Patients p ON a.PatientID = p.PatientID
        ORDER BY i.InvoiceDate DESC
    """)
    invoices = cursor.fetchall()

    # Fetch all staff for the "Add Salary" dropdown
    cursor.execute("SELECT UserID, Username FROM Users WHERE Role IN ('doctor', 'admin', 'accountant')")
    staff_users = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('accounts/dashboard.html', 
                           expenses=expenses, 
                           salaries=salaries, 
                           invoices=invoices, 
                           staff_users=staff_users)

@accounts_bp.route('/expense/add', methods=['POST'])
def add_expense():
    category = request.form['category']
    amount = request.form['amount']
    description = request.form['description']
    expense_date = request.form['expense_date']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO Expenses (Category, Amount, Description, ExpenseDate, RecordedByUserID)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (category, amount, description, expense_date, current_user.id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Expense record added successfully!', 'success')
    return redirect(url_for('accounts.dashboard'))

@accounts_bp.route('/salary/add', methods=['POST'])
def add_salary():
    user_id = request.form['user_id']
    amount = request.form['amount']
    payment_date = request.form['payment_date']
    notes = request.form['notes']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Salaries (UserID, Amount, PaymentDate, Notes) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (user_id, amount, payment_date, notes))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash('Salary payment recorded successfully!', 'success')
    return redirect(url_for('accounts.dashboard'))

@accounts_bp.route('/invoice/pdf/<int:invoice_id>')
def generate_invoice_pdf(invoice_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Query to get all necessary details for the invoice
    query = """
    SELECT 
        i.InvoiceID, i.TotalAmount, i.InvoiceDate, i.Status,
        a.AppointmentDateTime,
        p.FirstName AS PatientFirstName, p.LastName AS PatientLastName, p.Address,
        d.FirstName AS DoctorFirstName, d.LastName AS DoctorLastName
    FROM Invoices i
    JOIN Appointments a ON i.AppointmentID = a.AppointmentID
    JOIN Patients p ON a.PatientID = p.PatientID
    JOIN Doctors d ON a.DoctorID = d.DoctorID
    WHERE i.InvoiceID = %s;
    """
    cursor.execute(query, (invoice_id,))
    invoice_data = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not invoice_data:
        return "Invoice not found", 404
        
    # Render the dedicated HTML template for the PDF
    rendered_html = render_template('accounts/invoice_pdf.html', invoice=invoice_data)
    
    # Generate the PDF from the rendered HTML
    pdf = HTML(string=rendered_html).write_pdf()
    
    # Return the PDF as a response to the browser
    return Response(pdf, mimetype='application/pdf', headers={
        'Content-Disposition': f'inline; filename=invoice_{invoice_id}.pdf'
    })