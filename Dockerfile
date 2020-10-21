FROM python:3.7-slim 

COPY ./requirements.txt /home/test/requirements.txt
RUN pip install -r /home/test/requirements.txt

EXPOSE 5057

COPY ./app /home/test/app

CMD uvicorn home.test.app.main:app --host 0.0.0.0 --port 5057
