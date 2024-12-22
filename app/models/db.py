

import os

environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get('SCHEMA')



def add_prefix_for_prod(attr):
    if environment == "production":
        return f"{SCHEMA}.{attr}"
    else:
        return attr