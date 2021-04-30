# CAPy
A Certificate Authority microservice that can generate server/client certificates through an API interface

It currently does not provide any kind of authentication mechanism, so NAC and container network configuration are extremely important in deploying this service.

Basic API calls provided:

- GET root CA certificate for establishing trust
- GET new host certificate signed by CA
