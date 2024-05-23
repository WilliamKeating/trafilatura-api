# run image
FROM python:3.12-slim

WORKDIR /app

# install dependency
RUN apt update
RUN apt install -y python-dev build-essential

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.app:app"]
