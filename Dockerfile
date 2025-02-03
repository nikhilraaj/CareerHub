# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask app (with gunicorn for production)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
