FROM python:3.10.4

WORKDIR /app

COPY  ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

CMD [ "python", "./app.py"]
