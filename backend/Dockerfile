# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . /app/

# Expose the port that Flask will run on
EXPOSE 8080

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
