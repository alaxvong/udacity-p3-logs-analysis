#!/usr/bin/env python3
import psycopg2


# Query database
def make_query(query):
    # Connect to "news" PostgreSQL database, create a cursor, return query
    db = psycopg2.connect(database="news")
    c = db.cursor()
    c.execute(query)
    return c.fetchall()
    db.close()


question_1 = '1. What are the most popular three articles of all time?'
query_1 = '''
    SELECT title, count(*) AS num
    FROM articles, log
    WHERE log.path = CONCAT('/article/', articles.slug)
    GROUP BY articles.title
    ORDER BY num DESC
    LIMIT 3;'''

question_2 = '2. Who are the most popular article authors of all time?'
query_2 = '''
    SELECT name, count(path) AS hits
    FROM articles, log, authors
    WHERE log.path = CONCAT('/article/', articles.slug)
    AND articles.author = authors.id
    GROUP BY name
    ORDER BY hits DESC;'''

question_3 = '3. On which days did more than 1% of requests lead to errors?'
query_3 = '''
    SELECT *
    FROM
        (SELECT date(TIME), round(100.0*sum(CASE log.status
            WHEN '200 OK'
            THEN 0
            ELSE 1
        END)/count(log.status), 3) AS error
        FROM log
        GROUP BY date(TIME)
        ORDER BY error DESC) AS subq
    WHERE error > 1;'''


def print_views(question, query):
    # Print view query format
    results = make_query(query)
    print('\n' + question + '\n')
    for result in results:
        print('\t\u2022 ' + str(result[0]) + ' \u2014 ' +
              str(result[1]) + ' views')


def print_errors(question, query):
    # Print error query format
    results = make_query(query)
    print('\n' + question + '\n')
    for result in results:
        print('\t\u2022 ' + str(result[0].strftime('%B %d, %Y')) + ' \u2014 ' +
              str(result[1]) + '% errors')


if __name__ == "__main__":
    print_views(question_1, query_1)
    print_views(question_2, query_2)
    print_errors(question_3, query_3)
