FROM python:3.8-slim-buster

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

#CMD [ "python3", "-m" , "flask", "--app", "api", "--debug", "run", "--host=0.0.0.0"]

ENTRYPOINT [ "python3" ]
CMD ["api/app.py"]
