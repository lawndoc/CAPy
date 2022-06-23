### Builder image
# using ubuntu LTS version
FROM lsiobase/ubuntu:focal AS builder-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

# install python
RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3.9-dev python3.9-venv python3-pip python3-wheel build-essential && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
# using final folder name to avoid path issues with packages
RUN python3.9 -m venv /home/abc/venv
ENV PATH="/home/abc/venv/bin:$PATH"

# install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

### Runner image
FROM lsiobase/ubuntu:focal AS runner-image

# DEFAULT ARGS that can be changed
ARG SECRET_KEY="super_secret_default_key"
ARG CA_CERT_DIR="/opt/CAPy/CA"
ARG CA_NAME="CAPy Root CA"
ARG PROXY_DOMAIN="example.com"

# set environment variables
ENV SECRET_KEY=$SECRET_KEY
ENV CA_CERT_DIR=$CA_CERT_DIR
ENV CA_NAME=$CA_NAME
ENV PROXY_DOMAIN=$PROXY_DOMAIN

# install python
RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3-venv && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# use unprivileged user and virtual environment
RUN chsh -s /bin/bash abc
COPY --from=builder-image /home/abc/venv /home/abc/venv

# create directory for runtime and switch to user
RUN mkdir -p ${CA_CERT_DIR}
WORKDIR ${CA_CERT_DIR}/..
COPY . .

# expose port
EXPOSE 5000
# mark CA store as volume and set permissions
VOLUME ${CA_CERT_DIR}
RUN echo chown -R abc:abc ${CA_CERT_DIR}/.. >> /etc/cont-init.d/10-adduser

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/home/abc/venv
ENV PATH="/home/abc/venv/bin:$PATH"

# /dev/shm is mapped to shared memory and should be used for gunicorn heartbeat
# this will improve performance and avoid random freezes
CMD ["su", "-c", "'sh run.sh'", "abc"]