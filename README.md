# CareerHub Application

This project is a web-based CareerHub Application built with Flask and MongoDB, allowing users to manage and track programming questions.

The CareerHub Application is designed to help users organize and track their progress on programming questions. It provides a platform for users to add, edit, delete, and mark questions as completed. The system is built with Flask, a lightweight Python web framework, and uses MongoDB as its database backend.

Key features of the system include:
- User authentication (registration and login)
- Adding new questions with topics, titles, and practice links
- Editing existing questions
- Deleting questions
- Marking questions as completed
- Viewing all questions sorted by topic
Visit the project: [https://www.careerhubs.info/](https://www.careerhubs.info/)

The application uses Flask-Session for session management and Werkzeug for password hashing, ensuring secure user authentication. PyMongo is used as the Python driver for MongoDB, allowing seamless interaction with the database.

## Repository Structure

```
.
├── app.py
├── requirements.txt
└── templates
    ├── index.html
    ├── login.html
    ├── qsn.html
    └── register.html
```

- `app.py`: The main Flask application file containing all route definitions and business logic.
- `requirements.txt`: Lists all Python dependencies required for the project.
- `templates/`: Directory containing HTML templates for rendering pages.
  - `index.html`: The home page template.
  - `login.html`: The login page template.
  - `qsn.html`: The template for displaying all questions.
  - `register.html`: The user registration page template.


## Data Flow

The CareerHub Application follows a typical client-server architecture with Flask handling the server-side logic and MongoDB serving as the database. Here's an overview of the data flow:

1. User sends a request (e.g., view questions, add a question) via the web browser.
2. The request is received by the Flask application (`app.py`).
3. Flask routes the request to the appropriate function based on the URL and HTTP method.
4. The function interacts with the MongoDB database using PyMongo to perform CRUD operations.
5. The result is processed and rendered using an HTML template or returned as JSON.
6. The response is sent back to the user's browser.

```
[User] <-> [Web Browser] <-> [Flask App (app.py)] <-> [PyMongo] <-> [MongoDB]
```

Important technical considerations:
- User authentication state is maintained using Flask sessions.
- Passwords are hashed before storage for security.
- MongoDB queries are performed using PyMongo's methods to ensure proper data handling.
