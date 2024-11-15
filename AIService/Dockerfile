FROM python:3.11.10-slim as base
WORKDIR /app
LABEL org.opencontainers.image.source https://github.com/jezvgg/City-Guide

EXPOSE 8000

COPY ./Model /app/Model
COPY ./main.py /app/main.py
COPY ./service.py /app/service.py
COPY ./swagger.yml /app/swagger.yml
COPY ./req_productaion.txt /app/req_productaion.txt

RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list \
    && apt-get update && apt-get install -y --no-install-recommends -o APT::Immediate-Configure=false gcc g++

RUN pip install Cython
RUN pip install -r req_productaion.txt
ENTRYPOINT python3 /app/main.py