# Use latest official Python image
FROM python:3.12-slim

# Set work directory
WORKDIR /training-app

# Copy your root files
COPY training-app.py /training-app/training-app.py
COPY config.py /training-app/config.py
COPY log_config.py /training-app/log_config.py
COPY logging.yaml /training-app/logging.yaml
COPY requirements.txt /training-app/requirements.txt
COPY README.md /training-app/README.md

# Copy the complete "static" Folder
COPY static/ /training-app/static/

# Copy the complete "templates" Folder
COPY templates/ /training-app/templates/

# Copy the entire 'training_sets' folder into the container's /training-app directory
COPY training_sets/ /training-app/training_sets/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Flask (default is 5000)
EXPOSE 5000

# Start the Flask app
CMD ["python", "training-app.py"]
