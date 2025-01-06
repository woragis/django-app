FROM python

# Set environment variables to ensure Python outputs are unbuffered and any errors are raised immediately
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt to the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files into the container
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# Run Django's development server by default
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
