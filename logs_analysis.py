#!/usr/bin/env python3
import psycopg2


# Query database
def make_query(query):
    db = psycopg2.connect(database="news")
    c = db.cursor()
    c.execute(query)
    return c.fetchall()
    db.close()


# 1. What are the most popular three articles of all time?
query1 = '''
    SELECT title,count(*) AS num
    FROM articles, log
    WHERE log.path=CONCAT('/article/', articles.slug)
    GROUP BY articles.title
    ORDER BY num DESC
    LIMIT 3;'''

# 2. Who are the most popular article authors of all time?
query2 = '''
    SELECT authors.name, sum(numviews_view.num) AS views
    FROM numviews_view, authors
    WHERE authors.id=numviews_view.author
    GROUP BY authors.name
    ORDER BY views DESC;'''

# 3. On which days did more than 1% of requests lead to errors?
query3 = '''
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


def print_query_1_results(query):
    results = make_query(query)
    print('\n1. The 3 most popular articles of all time are:\n')
    for result in results:
        print('\t\u2022 ' + str(result[0]) + ' \u2014 ' +
              str(result[1]) + ' views')


def print_query_2_results(query):
    results = make_query(query)
    print('\n2. The most popular article authors of all time are:\n')
    for result in results:
        print('\t\u2022 ' + str(result[0]) + ' \u2014 ' +
              str(result[1]) + ' views')


def print_query_3_results(query):
    results = make_query(query)
    print('\n3. Days with more than 1% of request that lead to an error:\n')
    for result in results:
        print('\t\u2022 ' + str(result[0].strftime('%B %d, %Y')) + ' \u2014 ' +
              str(result[1]) + '%' + ' errors')


print_query_1_results(query1)
print_query_2_results(query2)
print_query_3_results(query3)