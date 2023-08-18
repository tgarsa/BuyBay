FROM tiangolo/uvicorn-gunicorn:python3.8-slim 

WORKDIR /app 
ENV DEBIAN_FRONTEND=noninteractive
ENV MODULE_NAME=app

ADD requirements.txt .

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5010"]
