### Builder image
# using ubuntu LTS version
FROM ubuntu:20.04 AS builder-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

# install python
RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3.9-dev python3.9-venv python3-pip python3-wheel build-essential && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
# using final folder name to avoid path issues with packages
RUN python3.9 -m venv /home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"

# install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

### Runner image
FROM ubuntu:20.04 AS runner-image

# DEFAULT ARGS that can be changed
ARG SECRET_KEY="super_secret_default_key"
ARG CA_CERT_DIR="/opt/CAPy/CA"
ARG CA_NAME="CAPy Root CA"

# set environment variables
ENV SECRET_KEY=$SECRET_KEY
ENV CA_CERT_DIR=$CA_CERT_DIR
ENV CA_NAME=$CA_NAME

# install python
RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3-venv && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# create unprivileged user and virtual environment
RUN useradd --create-home myuser
COPY --from=builder-image /home/myuser/venv /home/myuser/venv

# copy code over
USER myuser
RUN mkdir ${CA_CERT_DIR}
WORKDIR ${CA_CERT_DIR}/..
COPY . .

# expose port and mount CA volume
EXPOSE 5000
VOLUME /opt/CAPy/CA

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"

# /dev/shm is mapped to shared memory and should be used for gunicorn heartbeat
# this will improve performance and avoid random freezes
CMD ["gunicorn","-b", "0.0.0.0:5000", "-w", "4", "-k", "gevent", "--worker-tmp-dir", "/dev/shm", "api:app"]