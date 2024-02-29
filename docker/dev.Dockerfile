FROM python:3.8

WORKDIR /opt/savingface/

COPY . /opt/savingface/

RUN pip install --no-cache-dir -r ./requirements.txt
