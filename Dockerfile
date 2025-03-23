# Base Image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 8000

# Run Gunicorn server
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]

