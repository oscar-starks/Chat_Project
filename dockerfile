FROM python:3.10.4
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Redis
RUN apt-get update && \
    apt-get install -y redis-server && \
    apt-get clean

# Set the working directory in the container
WORKDIR /code

# Copy requirements.txt and install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /code/

# Expose ports
EXPOSE 8000 6379

# Start Django server and Redis server
CMD ["sh", "-c", "service redis-server start && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
