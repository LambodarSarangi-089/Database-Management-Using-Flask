-- Drop the existing database if it exists
DROP DATABASE IF EXISTS flask_auth;

-- Create the database
CREATE DATABASE flask_auth;

-- Use the database
USE flask_auth;

-- Drop existing tables if they exist (in case of any leftovers)
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS users;

-- Create the users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the subjects table
CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL UNIQUE
);

-- Insert predefined subjects
INSERT INTO subjects (subject_name) VALUES
('VLSI'),
('Computer Networks'),
('DSA'),
('Software Engineering'),
('Communication Engineering'),
('Operating System');

-- Create the grades table
CREATE TABLE grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subject_id INT NOT NULL,
    grade CHAR(1) NOT NULL,  -- Grades like A, B, C, etc.
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);

-- Create the documents table
CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Verify the data
SELECT * FROM users;
SELECT * FROM subjects;
SELECT * FROM grades;