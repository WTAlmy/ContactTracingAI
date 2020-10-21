FROM python:3.7-slim 

COPY ./requirements.txt /home/test/requirements.txt
RUN pip install -r /home/test/requirements.txt

COPY ./app /home/test/app

CMD celery worker -A home.test.app.worker.celery_worker -l info -Q test-queue
