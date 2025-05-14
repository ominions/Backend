# use official python image
FROM python:3.12.9-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set workingdir inside the container
WORKDIR /code

# Install system dependencies
RUN apt update && apt install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /code/

# RUN migrations and start server by default (optional CMD, can be overridden)
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

#for prod
# CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]