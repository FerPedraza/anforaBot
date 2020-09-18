FROM python:3.7.5

RUN pip install -U pip
RUN pip install gunicorn
RUN python3 -m pip install --upgrade pip

WORKDIR /chatbots-frameworkbot

COPY . .

RUN pip install -r requirements.txt
