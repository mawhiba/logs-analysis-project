#!/usr/bin/env python 2.7.12
#
# This code is executing 3 SQL queries :
# 1. What are the most popular three articles of all time?
# 2. Who are the most popular article authors of all time?
# 3. On which days did more than 1% of requests lead to errors?
#
# /////////////////////////////////////////////////////////////

import psycopg2

# Connect to the database
db = psycopg2.connect("dbname=news")
a = db.cursor()
b = db.cursor()
c = db.cursor()

#1. What are the most popular three articles of all time?
a.execute("select title, count(path) as num from articles as a, log as l where a.slug = substring(l.path from 10) group by a.title order by num desc limit 3;")
for row in a.fetchall():
    print(row)

print("\n")

# 2. Who are the most popular article authors of all time?
b.execute("select aut.name, sum(subq.num) as Total_Views from authors as aut, (select author, title, count(path) as num from articles as a, log as l where a.slug = substring(l.path from 10) group by a.title, a.author order by num desc) as subq where aut.id = subq.author group by aut.name order by Total_Views desc;")
for row in b.fetchall():
    print(row)

print("\n")

# 3. On which days did more than 1% of requests lead to errors?
c.execute("select to_char(t2::date,'Mon dd, yyyy') as Day, round((num1::decimal/num2)*100,2) as errorPercentage from log, (select time::timestamp::date as t2, count(path) as num2 from log group by t2 order by t2)as DailyRequest, (select time::timestamp::date as t3, count(path) as num1 from log where status like '404 NOT FOUND' group by t3 order by t3) as DailyErrors where DailyRequest.t2 = DailyErrors.t3 and  (num1::decimal/num2)*100 > 1 group by t2,t3,DailyRequest.num2,DailyErrors.num1 order by t2;")
for row in c.fetchall():
    print(row)
db.close()
