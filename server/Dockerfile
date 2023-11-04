FROM python:3.10.12
WORKDIR /server
COPY . /server
#RUN apt-get update && \
#    apt-get install python3-dev -y && \
#    pip3 install --upgrade pip && \
#    pip3 install -r requirements.txt
RUN pip3 install --upgrade cython && \
    pip3 install -r requirements.txt
EXPOSE 5683
CMD ["python3", "server.py"]

