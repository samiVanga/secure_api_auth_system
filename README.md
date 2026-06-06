# Secure API Authentication System

A secure Flask-based API authentication system that allows users to register, log in and receive JWT access tokens. The project includes password hashing, JWT authentication, rate limiting, password validation, database storage, and a simple frontend built with HTML, CSS, and JavaScript.

## Features

* User registration
* User login
* Secure password hashing using Bcrypt
* JWT-based authentication
* Protected routes
* User-specific notes
* Password strength validation
* Rate limiting for login and registration routes
* SQLite database using SQLAlchemy
* Simple frontend interface
* Configuration file for secret keys and database settings

## Technologies Used

* Python
* Flask
* Flask-SQLAlchemy
* Flask-JWT-Extended
* Flask-Bcrypt
* Flask-Limiter
* Flask-CORS
* HTML
* CSS
* JavaScript
* SQLite

## Project Structure

```text
secure_api_auth_system/
│
├── app.py
├── config.py
├── .gitignore
├── README.md
│
├── templates/
│   ├── index.html
│   └── register.html
│
└── static/
    ├── style.css
    └── script.js
```

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd secure_api_auth_system
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install flask flask_sqlalchemy flask_jwt_extended flask_bcrypt flask_limiter flask_cors
```

## Configuration

Create a `config.py` file in the root directory:

```python
JWT_SECRET_KEY = "your-secret-key-here"
SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
```

You can generate a secure JWT secret key using:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Make sure `config.py` is included in `.gitignore` so that secret keys are not pushed to GitHub.

## Running the Application

Run the Flask app:

```bash
python app.py
```

Then open the application in your browser:

```text
http://127.0.0.1:5000/
```

## API Endpoints

### Home Page

```http
GET /
```

Displays the login page.

### Register Page

```http
GET /register-page
```

Displays the registration page.

### Register User

```http
POST /register
```

Registers a new user.

Example request body:

```json
{
  "username": "testuser",
  "password": "Password123!"
}
```

Example response:

```json
{
  "message": "User registered successfully"
}
```

### Login User

```http
POST /login
```

Logs in an existing user and returns a JWT access token.

Example request body:

```json
{
  "username": "testuser",
  "password": "Password123!"
}
```

Example response:

```json
{
  "message": "Login Success",
  "access_token": "jwt-token-here"
}
```

### Protected Route

```http
GET /protected
```

Requires a valid JWT token.

Example header:

```http
Authorization: Bearer <access_token>
```

Example response:

```json
{
  "message": "Access granted for user 1"
}
```

## Password Validation

The application checks that registered passwords meet security requirements. A valid password should:

* Be at least 8 characters long
* Contain at least one uppercase letter
* Contain at least one lowercase letter
* Contain at least one number
* Contain at least one special character

Example valid password:

```text
Password123!
```

## Security Features

This project includes several security-focused features:

* Passwords are hashed using Bcrypt before being stored.
* Plain-text passwords are never saved in the database.
* JWT tokens are used for protected routes.
* Login and registration routes are rate-limited to reduce brute-force attempts.
* Secret keys are stored in a separate configuration file.
* `config.py` is excluded from GitHub using `.gitignore`.

## Author

Created by Samiksha Vanga.
