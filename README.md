# CAPy
A Certificate Authority microservice that can generate server/client certificates through an API interface

It currently does not provide any kind of authentication mechanism, so NAC and container network configuration are extremely important in deploying this service.

Basic API calls provided:

- GET `/ca/root-trust` -> get root CA certificate for establishing trust
- GET `/ca/host-certificate` -> get new host certificate signed by CA

TODO / Not yet implemented:

- POST `/ca/csr` -> generic certificate signing request (optionally supply own public key)
- POST `/ca/revoke-certificate` -> revoke certificate
- GET `/ca/revoke-certificate` -> check if cert has been revoked
