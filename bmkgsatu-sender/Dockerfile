FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN useradd -m bmkgsatu
RUN chown -R bmkgsatu:bmkgsatu /app
USER bmkgsatu


