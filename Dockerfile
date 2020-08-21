FROM nvidia/cuda:11.0-base-ubuntu18.04

USER root
WORKDIR /home/app_user/app

RUN apt update && \
    apt install -y curl && \
    curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl


# Install prerequisities for Ansible
RUN apt-get update
RUN apt-get -y install python3 python3-nacl python3-pip libffi-dev ssh

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src /home/app_user/app
RUN chmod +x startup.sh

CMD ["./startup.sh"]
