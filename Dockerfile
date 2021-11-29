FROM python:3.8-buster

USER root
WORKDIR /app
COPY . /app

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get install -y vim less

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN pip install -r requirements.txt

ENV PORT 80
CMD ["python", "app.py"]

# install heroku cli
RUN curl https://cli-assets.heroku.com/install.sh | sh
