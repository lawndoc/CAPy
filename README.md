# CAPy
A Certificate Authority microservice that can generate server/client certificates through an API interface

![Build/Tests](https://github.com/lawndoc/CAPy/actions/workflows/build-test.yml/badge.svg)
[![Codecov](https://codecov.io/gh/lawndoc/CAPy/branch/main/graph/badge.svg)](https://codecov.io/gh/lawndoc/CAPy)

It currently does not provide any kind of authentication mechanism, so NAC and container network configuration are extremely important in deploying this service.

## Functionality

Basic API calls provided:

- GET `/ca/root-trust` -> get root CA certificate for establishing trust
- GET `/ca/host-certificate` -> get new host certificate signed by CA

TODO / Not yet implemented:

- POST `/ca/csr` -> generic certificate signing request (optionally supply own public key)
- POST `/ca/revoke-certificate` -> revoke certificate
- GET `/ca/revoke-certificate` -> check if cert has been revoked
- OCSP server for clients to check if cert has been revoked via OCSP

## Deployment

CAPy requires the following environment variables to run properly:

| Variable Name | Description | Required | Default Value |
| --- | --- | --- | --- |
| CA_NAME | Name of the certificate authority | No | CAPy Root CA |
| CA_CERT_DIR | Directory within the container to save certificates | No | /opt/CAPy/CA |
| PROXY_DOMAIN | Domain that the CA is creating certificates for | Yes | |
| PGID | Container user GID; used for volume file permissions | Yes | |
| PUID | Container user UID; used for volume file permissions | Yes | |
| SECRET_KEY | Secret key for encryption; make sure this value is complex and protected | Yes | |

CAPy also requires a volume mounted at the CA_CERT_DIR location to be able to persist certificates across runs.

The following docker-compose file provides example deployment code:

```
version: "3.9"
services:
  capy:
    container_name: "capy"
    image: ghcr.io/lawndoc/capy:main
    volumes:
      - ./volumes/capy:/opt/CAPy/CA     # make sure this matches CA_CERT_DIR
    networks:
      - backend
    restart: always
    environment:
      CA_NAME: "MyOrg CA"               # optional
      CA_CERT_DIR: "/opt/CAPy/CA"       # optional
      PGID: 1001
      PROXY_DOMAIN: example.com
      PUID: 1000
      SECRET_KEY: ${SECRET_KEY}
networks:
  backend:
```
