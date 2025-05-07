# FROM python:3.10

# WORKDIR /app
# COPY . /app

# RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# RUN useradd -m bmkgsatu
# RUN chown -R bmkgsatu:bmkgsatu /app
# USER bmkgsatu

FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# UID bmkgsatu is 1000, dan GID awosftp is 1001
ARG UID=1000
ARG GID=1003
RUN groupadd -g $GID rasonftp && \
    useradd -m -u $UID -g $GID bmkgsatu

# Change ownership to the correct user and group
RUN chown -R bmkgsatu:rasonftp /app

USER bmkgsatu
