FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD [ "python", "./app.py" ]
CMD ["/usr/local/bin/gunicorn", "--workers=2", "--bind=0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
