# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY sample_submissions/solution.py solution.py
COPY sample_tests/test.py test.py

#RUN pip3 install -r requirements.txt

#COPY . .

CMD [ "python3", "-m" , "unittest", "test.SortTests"]