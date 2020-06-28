"""Here are all the constants needed."""
# database
standard_db = "postgres"
username_db = "postgres" # your username for psql
password_db = "" # your password for psql

dbname = "" # database name

table_db1 = "Nederlands"
table_content1 = "id serial PRIMARY KEY, naam varchar, vraag1 varchar, vraag2 varchar, vraag3 varchar, datum timestamp"
table_values1 = "naam, vraag1, vraag2, vraag3, datum"

table_db2 = "Francais"
table_content2 = "id serial PRIMARY KEY, nom varchar, question1 varchar, question2 varchar, question3 varchar, date timestamp"
table_values2 = "nom, question1, question2, question3, date"

# mail
username_mail = "" # email adress
password_mail = "" # password for email

imap = 'imap.gmail.com' # imap server

subject1 = "" # subject for mails of type 1
subject1_short = '' # shorter version for searching in imap
destination1 = "nederlands" # destination for the mails that are already read (for no doubles)

subject2 = ""
subject2_short = ''
destination2 = "frans"