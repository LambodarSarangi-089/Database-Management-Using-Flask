# Database-Management-Using-Flask

## 📝 Project Description
Database Management Using Flask is a full-stack web application built with Flask, MySQL, and SQLAlchemy that allows:

User registration and authentication

Secure password management (with hashing and reset)

Personal profile updates

Viewing academic grades (read-only)

Responsive and user-friendly interface

## 👨‍💻 Technologies Used
Backend: Flask, SQLAlchemy, Flask-Login

Frontend: HTML5, CSS3 (custom styles), Jinja2 templating

Database: MySQL

Security: Password hashing (Werkzeug)

## 🛠️ Setup & Run Instructions
# 1. Create and activate a virtual environment (recommended)
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# 2. Install required Python packages
pip install -r requirements.txt

# 3. Start MySQL Server and log into MySQL
#    Create a database named 'flask_auth':
#    CREATE DATABASE flask_auth;

# 4. Optionally, you can run the schema.sql file manually in your MySQL client to create tables
#    or let Flask handle it automatically (tables will be created on app start)

# 5. Run the Flask application
python app.py

# 6. Open your browser and go to:
http://127.0.0.1:5000


