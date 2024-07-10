FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7080

CMD ["python", "manage.py", "runserver", "0.0.0.0:7080"]
