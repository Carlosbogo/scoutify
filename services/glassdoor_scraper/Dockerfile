# We use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the environment variable to prevent Poetry from creating a virtual environment
ENV POETRY_VIRTUALENVS_CREATE=false

# Set the working directory in the container
WORKDIR /app

# Update the package list and install the Chromium browser
RUN apt-get update && \
    apt-get install -y chromium

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install poetry
RUN poetry install --no-root

# Expose port 80 to allow external access
EXPOSE 80

# The application starts by running the app.py file
CMD ["python", "app.py"]