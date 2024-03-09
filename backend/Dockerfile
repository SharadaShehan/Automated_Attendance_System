# Use Ubuntu image as base
FROM debian:bullseye

# Update package lists
RUN apt-get update

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory in the container
WORKDIR /app

# Install python virtual environment library
RUN apt-get install python3.11-venv -y

# Create a virtual environment named venv
RUN python3 -m venv venv

# Activate the virtual environment
RUN source venv/bin/activate

# Upgrade pip and install dependencies from requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install additional development dependencies
RUN apt-get install python3.11-dev* -y

# Install g++ and cmake (needed for face_recognition)
RUN apt-get install g++ cmake -y

# Install face_recognition library
RUN pip3 install face_recognition

# Set environment variables directly
ENV DEBUG=1
ENV SECRET_KEY='secret-key-of-django-app'
ENV HUB_SECRET_KEY=secret-key-of-hub-app
ENV DJANGO_ALLOWED_HOSTS=localhost
ENV SQL_ENGINE=django.db.backends.postgresql
ENV SQL_DATABASE=database-name
ENV SQL_USER=database-user
ENV SQL_PASSWORD=database-password
ENV SQL_HOST=database-host
ENV SQL_PORT=database-port
ENV MIN_MINUTES_THRESHOLD=5

# Expose port (modify port number if needed)
EXPOSE 8000

# Run migrations, collect static files, and start the Django development server
CMD ["python", "manage.py", "makemigrations", "&&", "python", "manage.py", "migrate", "&&", "python", "manage.py", "runserver", "&"]
