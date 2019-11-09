FROM ubuntu:latest
WORKDIR /service/
RUN apt update -y && apt install -y software-properties-common  && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt install -y python3.7 build-essential python3-dev libpython3.7-dev python3-pip && python3.7 -m pip install pip
# Install dependencies
COPY requirements.txt requirements.txt
RUN python3.7 -m pip install -r requirements.txt 
COPY models models
COPY src src
COPY server.py server.py
CMD ["python3.7", "server.py"]
EXPOSE 5000

