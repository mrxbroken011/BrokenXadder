# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Run your application
CMD ["python", "app.py"]
