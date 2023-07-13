import os

import psycopg2
from dotenv import load_dotenv

import csv
from pathlib import Path
load_dotenv()


def load_records():
    this_dir = Path(__file__).parent
    airports = []
    with this_dir.joinpath('airports.csv').open(encoding='utf8') as f:
        reader = csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            airports.append((
                row['icao'],
                row['name'],
                row['city'],
                row['country']
            ))
    return airports

def connection_db():
    try:
        with psycopg2.connect(
                dbname=os.environ.get('DB_NAME'),
                user=os.environ.get('DB_USERNAME'),
                password=os.environ.get('DB_PASSWORD'),
                host=os.environ.get('DB_HOST'),
        ) as connection:

            cursor = connection.cursor()
            values = load_records()

            cursor.executemany("INSERT INTO airports (code, name, city, country) VALUES (%s, %s, %s, %s)", values)
            connection.commit()

    except Exception as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    connection_db()
