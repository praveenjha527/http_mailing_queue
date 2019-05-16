FROM python:3
RUN mkdir /srv
COPY . /srv
CMD [ "python", "./master.py" ]