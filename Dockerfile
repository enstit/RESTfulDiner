FROM python:3.11

LABEL author="Enrico Stefanel (me@enst.it)"

ENV FLASK_APP='/usr/src/app/app'

WORKDIR /tmp/

RUN apt update && apt install -y python3-dev cmake libblas3 liblapack3 liblapack-dev libblas-dev

ADD docker/requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /usr/src/app/

EXPOSE 5000

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]