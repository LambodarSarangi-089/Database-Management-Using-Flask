import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'your_mysql_username'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'your_mysql_password'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'your_database_name'
    MYSQL_CURSORCLASS = 'DictCursor'  # Optional: Enables dictionary-like query results

# Example usage to set the MySQL URI:
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}/{Config.MYSQL_DB}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['UPLOAD_FOLDER'] = 'uploads'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
