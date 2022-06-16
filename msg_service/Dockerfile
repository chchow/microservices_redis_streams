FROM python:3

RUN pip install redis
RUN pip install requests

RUN mkdir -p /app

ENV PYTHONPATH /app

CMD [ "python", "/app/msg_service/msg_service.py" ]