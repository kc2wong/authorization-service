#!/usr/bin/env python3

import connexion

from generated.openapi_server import encoder
from openapi_server.config import logging, mongdb, key_pair

def main():
    logging.config_logging()
    mongdb.get_database()
    key_pair.init_key_pair()

    app = connexion.App(__name__, specification_dir='../generated/openapi_server/openapi')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Authorization Service - OpenAPI 3.0'},
                pythonic_params=True)

    app.run(port=8080)


if __name__ == '__main__':
    main()