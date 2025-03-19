FROM python:3.13.1-slim

LABEL author="Enrico Stefanel (enrico.stefanel@studenti.units.it)"

ENV FLASK_APP='/usr/src/app/app'

WORKDIR /tmp/

RUN apt update && apt install -y python3-dev cmake libblas3 liblapack3 liblapack-dev libblas-dev

ADD requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /usr/src/app/

EXPOSE 5000

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]