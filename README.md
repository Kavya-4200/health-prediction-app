# Healthcare Prediction Application

A Flask-based healthcare prediction application that manages patient records and uses Google Gemini AI API to generate health risk assessments based on blood test parameters.

## Features

- Patient CRUD Operations
  - Create patient records
  - View patient details
  - Update patient information
  - Delete patient records

- AI/ML Integration
  - Integrated Google Gemini AI API
  - Generates health risk assessment and recommendations based on:
    - Glucose level
    - Hemoglobin level
    - Cholesterol level

- Data Validation
  - Validates email format
  - Prevents future date of birth
  - Ensures blood test values are numeric

- Database
  - SQLite database
  - SQLAlchemy ORM for database operations

- User Interface
  - Responsive UI using HTML, CSS, and Bootstrap


## Technology Stack

- Backend: Python, Flask
- Database: SQLite
- ORM: SQLAlchemy
- Frontend: HTML, CSS, Bootstrap
- AI Integration: Google Gemini API


## Project Structure
