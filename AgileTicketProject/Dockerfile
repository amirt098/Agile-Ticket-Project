FROM python:3.8

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

## Make port 8000 available to the world outside this container
#EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
