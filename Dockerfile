# Use a Python 3.9 image as the base image
FROM python:3.9.17-slim-bullseye

# Set a working directory for the app
WORKDIR /app

# Copy the application code into the container
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that FastAPI will run on
EXPOSE 8000

# Run the FastAPI application
CMD ["python", "run.py"]
