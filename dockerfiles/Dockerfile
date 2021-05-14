# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

#COPY submissions/sample_solution.py solution.py
#COPY tests/sample_test.py test.py

#RUN pip3 install -r requirements.txt

#COPY . .

# с этим разобраться, супер-процесс
CMD [ "python3", "-m" , "unittest", "test.SortTests"]