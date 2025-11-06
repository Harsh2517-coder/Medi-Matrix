<<<<<<< HEAD
# MediMatrix - Hospital Management System

A comprehensive, modern hospital management system built with Python Flask and MySQL. This application provides a complete role-based solution for managing hospital operations with beautiful, responsive UI design.

---

## 🌟 Features

### 🧑‍⚕️ Patient Portal
- **Modern Dashboard** - Beautiful card-based appointment history with status indicators
- **Book Appointments** - Intuitive form with dynamic doctor selection based on specialization
- **Search & Filter** - Real-time search and pagination for appointment history
- **Appointment Tracking** - View appointment status (Pending, Confirmed, Completed, Cancelled)
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices

### 🩺 Doctor Portal
- **Appointment Management** - View all appointments with patient details
- **Patient List** - Access comprehensive patient records
- **Salary History** - Beautiful timeline view of salary payments
- **Modern UI** - Glassmorphism design with smooth animations

### 💰 Accountant Portal
- **Expense Management** - Track and manage hospital expenses
- **Salary Management** - Record and manage staff salary payments
- **Invoice Generation** - Generate PDF invoices for patient appointments
- **Financial Overview** - Comprehensive financial dashboard

### 👑 Admin Portal
- **Dashboard Analytics** - Key metrics: doctors, patients, beds, pending appointments
- **Appointment Approval** - Review and approve/decline appointment requests with confirmation dialogs
- **Staff Management** - View all doctors and staff members
- **Search & Pagination** - Advanced filtering and pagination for appointment requests
- **Real-time Updates** - Dynamic dashboard with live statistics

---

## 🛠️ Technology Stack

- **Backend:** Python 3.8+, Flask 3.1.0
- **Database:** MySQL 8.0+
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication:** Flask-Login
- **PDF Generation:** WeasyPrint
- **Styling:** Custom CSS with Glassmorphism effects, Gradient designs

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **MySQL Server 8.0+** - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
- **Git** (optional) - For cloning the repository
- **pip** - Python package manager (comes with Python)

### For Windows (PDF Generation):
If you're on Windows and need PDF generation, install GTK+ runtime:
- Download from [GTK+ for Windows](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Medi-Matrix-main
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

**Windows:**
```powershell
# Option 1: Use full Python path
C:\Users\mayan\AppData\Local\Programs\Python\Python311\python.exe -m pip install -r requirements.txt

# Option 2: If Python is in PATH
python -m pip install -r requirements.txt
```

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

### Step 4: Database Setup

1. **Start MySQL Server**
   - Ensure MySQL is running on your system
   - Default port: 3306

2. **Create Database**
   - Open MySQL Workbench or MySQL Command Line
   - Run the SQL script located at: `text_files/SQL_Query_For_Table_Creation.txt`
   - This will create the database `DBMS_CP` and all required tables with sample data

3. **Configure Database Connection**
   - Open `db_config.py`
   - Update the connection details:
     ```python
     host='localhost'
     user='root'  # Your MySQL username
     password='your_password'  # Your MySQL password
     database='DBMS_CP'
     ```

### Step 5: Run the Application

**Windows (PowerShell/CMD):**
```powershell
# Option 1: Use full Python path
C:\Users\mayan\AppData\Local\Programs\Python\Python311\python.exe app.py

# Option 2: If Python is in PATH
python app.py

# Option 3: Double-click run.bat file
```

**macOS/Linux:**
```bash
python3 app.py
```

The application will start on `http://localhost:5000`

---

## 🔐 Default Login Credentials

The database setup script includes sample users for testing:

**Patient:**
- Username: `priya.sharma84`
- Password: `password123`

**Doctor:**
- Username: `dr.alok.gupta`
- Password: `password123`

**Admin:**
- Username: `admin.rk.sharma`
- Password: `password123`

**Accountant:**
- Username: `acct.vinod.mehra`
- Password: `password123`

> **⚠️ Security Note:** Change these default passwords in production!

---

## 📁 Project Structure

```
Medi-Matrix-main/
├── app.py                 # Main Flask application
├── db_config.py           # Database configuration
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── README.md             # This file
│
├── routes/               # Flask blueprints
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── patient.py       # Patient portal routes
│   ├── doctor.py        # Doctor portal routes
│   ├── admin.py         # Admin portal routes
│   └── accounts.py      # Accountant portal routes
│
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── index.html       # Home page
│   ├── patient/         # Patient templates
│   ├── doctor/          # Doctor templates
│   ├── admin/           # Admin templates
│   └── accounts/        # Accountant templates
│
├── static/              # Static files
│   ├── css/
│   │   └── style.css    # Global styles
│   └── js/
│       └── main.js      # JavaScript files
│
└── text_files/          # Database setup files
    └── SQL_Query_For_Table_Creation.txt
```

---

## 🎨 Key Features & UI Highlights

- **Modern Glassmorphism Design** - Beautiful frosted glass effects throughout
- **Responsive Layout** - Mobile-first design that works on all devices
- **Smooth Animations** - Elegant transitions and hover effects
- **Search & Pagination** - Advanced filtering for large datasets
- **Loading States** - Visual feedback during data loading
- **Empty States** - Helpful messages when no data is available
- **Confirmation Dialogs** - Prevent accidental actions
- **Status Indicators** - Color-coded badges for quick status recognition
- **Consistent Button Styling** - Unified design language across all pages

---

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file in the root directory:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=DBMS_CP
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Changing Port

To run on a different port, modify `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change port here
```

---

## 🐛 Troubleshooting

### "No module named 'flask'"
**Solution:** Install dependencies using `pip install -r requirements.txt`

### "Database connection error"
**Solutions:**
1. Ensure MySQL server is running
2. Verify credentials in `db_config.py`
3. Check if database `DBMS_CP` exists
4. Run the SQL setup script again

### "Port 5000 already in use"
**Solution:** 
- Stop other Flask applications
- Or change port in `app.py`: `app.run(debug=True, port=5001)`

### PDF Generation Issues (Windows)
**Solution:** Install GTK+ runtime from the link in Prerequisites section

### Virtual Environment Issues
**Solution:**
```bash
# Delete and recreate
rm -rf venv  # or rmdir /s venv on Windows
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 📝 Development Notes

### Adding New Features

1. **New Routes:** Add blueprint files in `routes/` directory
2. **New Templates:** Create HTML files in `templates/` directory
3. **Styling:** Use CSS variables defined in `base.html` for consistency
4. **Database:** Update SQL schema in `text_files/SQL_Query_For_Table_Creation.txt`

### Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

---

## 🔒 Security Considerations

⚠️ **Important Security Notes:**

1. **Password Storage:** Currently uses plain text passwords. For production, implement password hashing using `werkzeug.security.generate_password_hash()`
2. **Secret Key:** Change the secret key in `app.py` for production
3. **Database Credentials:** Use environment variables instead of hardcoding
4. **CSRF Protection:** Consider adding Flask-WTF for CSRF protection
5. **Input Validation:** Add server-side validation for all user inputs

---

## 📄 License

This project is open source and available for educational purposes.

---

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the code comments
3. Open an issue on the repository

---

## 🎯 Future Enhancements

- [ ] Password hashing implementation
- [ ] Email notifications
- [ ] Password reset functionality
- [ ] Advanced reporting and analytics
- [ ] Mobile app integration
- [ ] API endpoints for external integrations
- [ ] Multi-language support

---

**Built with ❤️ using Flask and modern web technologies**
=======
# Medi-Matrix
>>>>>>> f120e06e37d626f5490e5fda2aa9ee1f1b2a9ede
