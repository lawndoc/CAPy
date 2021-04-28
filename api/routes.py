from flask import request, send_file
from api import app


@app.route("/ca/root-trust", methods=["GET"])
def rootTrust():
    """ Return root CA certificate for setting up trust """
    pass


@app.route("/ca/host-certificate", methods=["GET", "POST"])
def hostCertificate():
    """ Generate and return a new host certificate or validate a host certificate """
    pass


@app.route("/ca/client-certificate", methods=["GET", "POST"])
def clientCertificate():
    """ Generate and return a new client certificate or validate a host certificate """
    pass
