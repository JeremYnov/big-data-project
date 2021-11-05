FROM python:3.8

# create destination directory
RUN mkdir -p /usr/src
WORKDIR /usr/src

# copy files
COPY crypto-data/test.py ./
COPY requirements.txt ./
COPY crypto-news/producer-news.py ./

RUN pip3 install -r requirements.txt

CMD ["python3","crypto-data/test.py","crypto-news/producer-news.py"]
