FROM python:2.7-slim as python

RUN pip install Pillow mapnik simplekml

CMD ["bash"]

ADD . /picmap