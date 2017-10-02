Logs Analysis
=

Python 3 source code containing PostgreSQL queries that answer the following questions for project 3 of the Udacity Full Stack Developer program.

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Getting Started

- Download and connect [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) to your database
```bash
psql -d news -f newsdata.sql
```

- Install dependency: psycopg2
```bash
pip install psycopg2
```
- execute code
```bash
python logs_analysis.py
```

## Version

- Version 0.2
