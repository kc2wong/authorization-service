from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

import platform

from openapi_server.config.mongdb import get_database
from openapi_server.config.logging import logger
from openapi_server.config.environment import get_environment

def init_key_pair():
    database = get_database()

    host = get_environment("NODE_NAME") or platform.node()
    filter = {"host": host}

    key_pair = database["key-pair"].find_one(filter)
    if key_pair is None:
        logger.info("Keypair not found for node {0}".format(host))
        # generate private/public key pair
        key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, key_size=2048)

        # get public key in OpenSSH format
        public_key = key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.PKCS1)

        # get private key in PEM container format
        pem = key.private_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())

        # decode to printable strings
        private_key_str = pem.decode('utf-8')
        public_key_str = public_key.decode('utf-8')

        data = {"host": host, "public": public_key_str, "private": private_key_str}
        database["key-pair"].insert_one(data)
