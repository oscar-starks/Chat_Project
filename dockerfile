FROM python:3.10.4
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy requirements.txt and install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /code/
