import psycopg2
import random
from dotenv import load_dotenv
import urllib.parse as urlparse
import os

load_dotenv()
dbpath = os.getenv("DATABASE_URL")
url = urlparse.urlparse(dbpath)
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

QUERY_STRING = "SELECT * from problems WHERE id = {}"
SELECT_STRING = "SELECT * from problems"
MARK_DONE_QUERY_STRING = "UPDATE problems SET published = '1' WHERE id = {}"
CREATE_TMP_TABLE = "CREATE TABLE IF NOT EXISTS tmp (id serial PRIMARY KEY, title varchar(255), url varchar(255))"
INSERT_TMP_TABLE = "INSERT INTO tmp (title, url) VALUES ('{}', '{}')"
SELECT_TMP_TABLE = "SELECT * from tmp"
DELETE_TMP_TABLE_ROWS = "DELETE FROM tmp"


def connection():
    con = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )

    cursor = con.cursor()

    cursor.execute(CREATE_TMP_TABLE)
    cursor.execute(SELECT_STRING)
    sz = len(cursor.fetchall())
    cursor.close()
    return con, sz


def get_problems():
    con, sz = connection()
    problem_list = []
    problem_idx = []
    ok = False
    number_of_problems = 3
    while not ok:
        temp = []
        l = random.sample(range(1, sz + 1), number_of_problems)
        for i in range(number_of_problems):
            cursor = con.cursor()
            cursor.execute(QUERY_STRING.format(l[i]))
            record = cursor.fetchall()
            cursor.close()
            temp.append(record[0])

        for x in temp:
            ok = ok and temp[-2]
        ok = not (ok)

        if ok:
            problem_list = temp
            problem_idx = l

    cursor = con.cursor()
    for idx in problem_idx:
        cursor.execute(MARK_DONE_QUERY_STRING.format(idx))
        cursor.execute(QUERY_STRING.format(idx))
    cursor.close()

    cursor = con.cursor()
    cursor.execute(DELETE_TMP_TABLE_ROWS)
    for x in problem_list:
        cursor.execute(INSERT_TMP_TABLE.format(x[1], x[3]))
    cursor.close()

    con.commit()
    con.close()


def get_problems_from_db():
    con, sz = connection()
    prob_list = []
    cursor = con.cursor()
    cursor.execute(SELECT_TMP_TABLE)
    for x in cursor.fetchall():
        prob_list.append(x)
    cursor.close()
    con.commit()
    con.close()
    return prob_list
