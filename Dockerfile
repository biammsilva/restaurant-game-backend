FROM python:3.8

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv install --system
EXPOSE 6789
COPY . /

CMD [ "python", "./server.py"]