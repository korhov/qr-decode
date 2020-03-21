FROM python:3.7

RUN apt-get update \
 && apt-get install -y python-qrtools libzbar-dev libzbar0 poppler-utils # poppler

RUN pip install -U matplotlib opencv-python pyzbar[scripts]

ENV HTTP_HOST 0.0.0.0
ENV HTTP_PORT 80
EXPOSE 80

RUN mkdir -p /home/qr

COPY requirements.txt /home/qr/requirements.txt

WORKDIR /home/qr/

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Makes sure zlib can be found and set variables for QR Text and Filename
ENV LIBRARY_PATH=/lib:/usr/lib

COPY main.py /home/qr/main.py
COPY decode /home/qr/decode/

CMD ["python", "./main.py"]
