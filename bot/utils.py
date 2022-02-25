import psycopg2
import random
import csv
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

con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )

cursor = con.cursor()

QUERY_STRING = "SELECT * from problems WHERE id = {}"
SELECT_STRING = "SELECT * from problems"
MARK_DONE_QUERY_STRING = "UPDATE problems SET published = '1' WHERE id = {}"

cursor.execute(SELECT_STRING)
sz = len(cursor.fetchall())
cursor.close()


def get_problems():
    problem_list = []
    problem_idx = []
    ok = False
    number_of_problems = 3
    while not ok:
        tmp = []
        l = random.sample(range(1, sz + 1), number_of_problems)
        for i in range(number_of_problems):
            cursor = con.cursor()
            cursor.execute(QUERY_STRING.format(l[i]))
            record = cursor.fetchall()
            cursor.close()
            tmp.append(record[0])

        for x in tmp:
            ok = ok and tmp[-2]
        ok = not (ok)

        if ok:
            problem_list = tmp
            problem_idx = l

    cursor = con.cursor()
    for idx in problem_idx:
        cursor.execute(MARK_DONE_QUERY_STRING.format(idx))
        cursor.execute(QUERY_STRING.format(idx))
    cursor.close()

    con.commit()
    con.close()

    with open("tmp/probs.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "URL"])
        for x in problem_list:
            writer.writerow([x[1], x[3]])


def get_problems_from_csv():
    prob_list = []
    with open("tmp/probs.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            prob_list.append(row)
    return prob_list[1:]
