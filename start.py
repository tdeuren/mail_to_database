"""This script logs in on the standard database of psql. Creates new database and creates the tables.
This should only run ones."""
import psycopg2 as ps
from constants import *
import os

""" 
to install:
    python (https://www.python.org/downloads/release/python-381/)
    psql (postgresql_installer)
    pip, psycopg2 (get-pip.py) (in cmd in directory van python: pip install psycopg2)
    pgadmin to check the database (postgresql_installer)

via cmd instead of this script:
    in cmd: psql -h localhost -U postgres -d postgres
    password psql: your password
    in psql: create database name_database; 
    create tables"""

# connect to standard database
conn = ps.connect("dbname=%s user=%s password=%s" %(standard_db, username_db, password_db))
conn.autocommit = True
cur = conn.cursor()
# create new database
try:
    cur.execute("Create database %s" %dbname)
    conn.commit()
except:
    print("could not create database")
# close connection
cur.close()
conn.close()
# connect to new database
conn = ps.connect("dbname=%s user=%s password=%s" %(dbname, username_db, password_db))
cur = conn.cursor()
# create table
cur.execute("CREATE TABLE %s (%s);" %(table_db1, table_content1))
cur.execute("CREATE TABLE %s (%s);" %(table_db2, table_content2))
conn.commit()
# close connection
cur.close()
conn.close()
