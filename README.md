# MediMatrix - Hospital Management System

A comprehensive hospital management system built with Python, Flask, and MySQL. This project features a complete, role-based web application that allows patients, doctors, accountants, and administrators to manage hospital operations efficiently.

---

## 🌟 Key Features

The application is divided into four distinct, secure portals based on user roles:

### 🧑‍⚕️ Patient Portal
* **View Medical History:** Access a complete history of past appointments, diagnoses, and prescriptions.
* **Book Appointments:** A user-friendly form to book new appointments.
* **Dynamic Selection:** Dropdown menus to select a specialization and then a specific doctor in that field.
* **Date Validation:** The calendar interface prevents booking appointments on past dates.

### 🩺 Doctor Dashboard
* **Appointment Management:** View a chronological list of all upcoming and past appointments.
* **Patient Records:** Access a list of all previously treated patients for quick history review.
* **Profile & Salary:** View personal profile information and salary payment history.

### 💰 Accounts Dashboard
* **Expense Management:** A comprehensive view to manage and track all hospital expenses.
* **Salary Management:** View and manage salary records for all staff and doctors.
* **PDF Invoice Generation:** Generate and view patient invoices as PDF files directly from the dashboard.

### 👑 Admin Dashboard
* **Operational Overview:** A dynamic dashboard displaying key metrics like doctor counts and pending appointments.
* **Appointment Scheduling:** View all incoming appointment requests from patients and approve or decline them.
* **Staff Management:** A complete list of all doctors and staff members with their details.

---

## 🛠️ Technology Stack

* **Backend:** Python 3, Flask
* **Database:** MySQL
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
* **PDF Generation:** WeasyPrint
* **Authentication:** Flask-Login

---

## 🚀 How to Run This Project

Follow these steps to get the project running locally.

### 1. Prerequisites
* Python 3.x
* Git
* A running MySQL Server

### 2. Clone & Setup
```bash
# Clone the repository
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name

# Create and activate a virtual environment (recommended)
python -m venv venv
# On Windows:
# venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install the required packages
pip install -r requirements.txt
