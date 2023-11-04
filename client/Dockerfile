FROM python:3.10.12
WORKDIR /client
COPY . /client
RUN pip3 install --upgrade cython && \
    pip3 install -r requirements.txt
EXPOSE 61616
CMD ["python3", "client.py"]

