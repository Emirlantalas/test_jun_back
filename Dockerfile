FROM python:3.10
WORKDIR /app
ENV DJANGO_SETTINGS_MODULE test_jun_back.settings
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
CMD ["python", "manage.py", "runserver", "http://127.0.0.1:8000"]