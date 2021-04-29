FROM python:3.9

# DEFAULT ARGS that can be changed
ARG SECRET_KEY="super_secret_default_key"
ARG CA_CERT_DIR="/opt/CAPy/CA"
ARG CA_NAME="CAPy Root CA"

# set environment variables
ENV SECRET_KEY=$SECRET_KEY
ENV CA_CERT_DIR=$CA_CERT_DIR
ENV CA_NAME=$CA_NAME

# copy code and install dependencies
COPY ./* /opt/CAPy/
RUN pip install -r /opt/CAPy/requirements.txt

# for documentation purposes --> still need to specify at runtime
EXPOSE 80:5000
VOLUME CAPy:/opt/CAPy/CA

# start app
ENTRYPOINT ["python", "/opt/CAPy/CAPy.py"]