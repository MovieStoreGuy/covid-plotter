FROM python:3.9.6-alpine

WORKDIR /src/covid-plotter

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]