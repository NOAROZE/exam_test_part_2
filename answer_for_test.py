# Part C – Executing SQL Queries in Python (10 points):
import psycopg2
import psycopg2.extras

try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='215069121',
        host='localhost',
        port='5432',
        cursor_factory=psycopg2.extras.RealDictCursor
    )
    print("Connected successfully.")
except psycopg2.Error as e:
    print("Connection error:", e)

cur = conn.cursor()


def select(query, vars):
    cur.execute(query, vars)
    return cur.fetchall()


def insert_data(query, data):
    cur.executemany(query, data)


try:
    result = select('select m.movie_name as movie_name from movies m;', ('',))
    for row in result:
        print(dict(row))
except psycopg2.Error as e:
    print("Error select from movies:", e)

print()

try:
    result = select('select m.movie_name as movie_name from movies m where m.movie_name like %s;'
                    , ('%' + 'to' + '%',))
    for row in result:
        print(dict(row))
except psycopg2.Error as e:
    print("Error select from movies:", e)

try:
    new_movie_name: str = input('Enter a movie name: ')
    new_genre: str = input('Enter a genre name: ')
    new_country: str = input('Enter a country: ')
    new_language: str = input('Enter a language: ')
    new_year: int = int(input('Enter a year: '))
    new_revenue: int = int(input('Enter a number of revenue: '))
    data = [
        (new_movie_name, new_genre, new_country, new_language, new_year, new_revenue)
    ]

    insert_data(
        '''insert into movies(movie_name, genre, country, language, year, revenue) values (%s, %s, %s, %s, %s, %s);''',
        data)
    conn.commit()
    print('Insert successfully.')

except Exception as e:
    conn.rollback()
    print("Insert failed. All changes rolled back.")
    print("Error:", e)

conn.close()
