FROM ubuntu
ARG aws_access_key_id
ARG aws_secret_access_key
ENV aws_access_key_id=$aws_access_key_id
ENV aws_secret_access_key=$aws_secret_access_key
RUN apt-get update
RUN apt-get -y install git
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN pip3 install boto3
RUN mkdir ~/.aws
RUN echo "[default]\naws_access_key_id = $aws_access_key_id\naws_secret_access_key = $aws_secret_access_key" > ~/.aws/credentials
RUN git clone https://github.com/PeterAdamson/PolicyCounter.git
RUN python3 PolicyCounter/PolicyCounter.py
