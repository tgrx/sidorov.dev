#!/usr/bin/env python3

import dj_database_url
from dynaconf import settings

URL = dj_database_url.parse(settings.DATABASE_URL)

HOST = URL["HOST"]
NAME = URL["NAME"]
PASSWORD = URL["PASSWORD"]
PORT = URL["PORT"]
USER = URL["USER"]

print(
    f"""
    ***     {PASSWORD}      ***
    
    psql -U {USER} -W -h {HOST} -p {PORT} -d {NAME}

    """
)
