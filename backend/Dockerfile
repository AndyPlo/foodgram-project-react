
FROM python:3.7-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY foodgram/ /app

WORKDIR /app

ENV SECRET_KEY="django-insecure-2=)*=0lkrp3k+b*518^co)t5--j#2x5d!qy*w3she)gh6+-q(e"

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
