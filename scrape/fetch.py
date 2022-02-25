from time import time
import requests
import json
import psycopg2
from dotenv import load_dotenv
import os
import urllib.parse as urlparse

load_dotenv()
dbpath = os.getenv("DATABASE_URL")
url = urlparse.urlparse(dbpath)
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port


API = "https://leetcode.com/api/problems/algorithms/"
BASE_URL = "https://leetcode.com/problems/"

res = requests.get(API)
res = json.loads(res.text)

print("Loaded JSON")

sql_file = open("scrape/schema.sql", "r")
SCHEMA = sql_file.read()

sql = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )
c = sql.cursor()
c.execute(SCHEMA)

idx = 1
for i in res["stat_status_pairs"]:
    name = str(i["stat"]["question__title"])
    slug = str(i["stat"]["question__title_slug"])
    url = BASE_URL + slug
    print(idx, name, slug, url)
    c.execute(
        """INSERT INTO problems VALUES (%s, %s, %s, %s, %s, %s)""", (idx, name, slug, url, False, str(time())),
    )
    idx += 1

sql.commit()
sql.close()
print("Done creating db!")
