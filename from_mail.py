""" This reads the mails with a specific subject and stores the information in the database.
This is specific for the type of mails this is written for. 
You have let less secure apps to your mails. (for google -> security settings)"""
import psycopg2 as ps
import imaplib, email
from constants import *

# connect to database
conn = ps.connect("dbname=%s user=%s password=%s" %(dbname, username_db, password_db))
# get cursor
cur = conn.cursor()

# connect to mailserver
mail = imaplib.IMAP4_SSL(imap, 993)
# try to login
try:
    mail.login(username_mail, password_mail)
except:
    print("Login failed")

# go to inbox
mail.select('Inbox')


# Nederlands ----------------------------------------------------------------------------------
# search all mails with subject subject
typ, [response] = mail.search(None, subject1_short)
# get all ids from mail from search 
msg_ids = ','.join(response.decode("utf-8").split(' '))
id_list = msg_ids.split(',')
#print(id_list)
# remove '' from empty list
if id_list[0] == '':
    id_list = []
# read every mail
for j in id_list:
    # id_list are strings, make int
    i = int(j)
    #print(j)
    # fetch mail i
    typ, data = mail.fetch( b'%d'%i, '(RFC822)' )
    for response_part in data:
        if isinstance(response_part, tuple):
            # get msg from bytes
            msg = email.message_from_bytes(response_part[1])
            # get subject and from from msg
            varSubject = msg['subject']
            varFrom = msg['from']
            if varSubject != subject1:
                print("Wrong mail to NL") # if selection of mails wasn't narrow enough
                break
            # get body from msg
            try:
                #print(varFrom)
                #print("\t", varSubject)
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        type = part.get_content_type()
                        disp = str(part.get('Content-Disposition'))
                        # look for plain text parts, but skip attachments
                        if type == 'text/plain' and 'attachment' not in disp:
                            charset = part.get_content_charset()
                            # decode the base64 unicode bytestring into plain text
                            body = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                            # if we've found the plain/text part, stop looping thru the parts
                            break
                else:
                    # not multipart - i.e. plain text, no attachments
                    charset = msg.get_content_charset()
                    body = msg.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                # get the right parts for the database
                body = body.replace('\r', '').replace('\t', '').split('\n')
                body = [i.strip() for i in body if i != '']
                # get information
                naam = body[2]
                vraag1 = body[4]
                vraag2 = body[6]
                vraag3 = body[8]
                datum = body[10]
                #print(naam)
                #print(vraag1)
                #print(vraag2)
                #print(vraag3)
                #print(datum)
                # insert values in database
                cur.execute("INSERT INTO %s (%s) VALUES ('%s', '%s', '%s', '%s',timestamp '%s');" %(table_db1, table_values1, naam, vraag1, vraag2, vraag3, datum))
                #print("inserted")
                # commit the action
                conn.commit()
            except:
                print("\tSomething went wrong")
#print("\n")
# set all the read mails in map destination (copy to map, store in bin)
if len(msg_ids) > 0:
    mail.copy(msg_ids, destination1)
    mail.store(msg_ids, '+FLAGS', r'(\Deleted)')


# Francais ----------------------------------------------------------------------------------
# search all mails with subject subject
typ, [response] = mail.search(None, subject2_short)
# get all ids from mail from search 
msg_ids = ','.join(response.decode("utf-8").split(' '))
id_list = msg_ids.split(',')
#print(id_list)
# remove '' from empty list
if id_list[0] == '':
    id_list = []
# read every mail
for j in id_list:
    # id_list are strings, make int
    i = int(j)
    #print(j)
    # fetch mail i
    typ, data = mail.fetch( b'%d'%i, '(RFC822)' )
    for response_part in data:
        if isinstance(response_part, tuple):
            # get msg from bytes
            msg = email.message_from_bytes(response_part[1])
            # get subject and from from msg
            varSubject = msg['subject']
            varFrom = msg['from']
            if varSubject != subject2:
                print("Wrong mail to FR")
                break
            # get body from msg
            try:
                #print(varFrom)
                #print("\t", varSubject)
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        type = part.get_content_type()
                        disp = str(part.get('Content-Disposition'))
                        # look for plain text parts, but skip attachments
                        if type == 'text/plain' and 'attachment' not in disp:
                            charset = part.get_content_charset()
                            # decode the base64 unicode bytestring into plain text
                            body = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                            # if we've found the plain/text part, stop looping thru the parts
                            break
                else:
                    # not multipart - i.e. plain text, no attachments
                    charset = msg.get_content_charset()
                    body = msg.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                # get the right parts for the database
                body = body.replace('\r', '').replace('\t', '').split('\n')
                body = [i.strip() for i in body if i != '']
                # get information
                naam = body[2]
                vraag1 = body[4]
                vraag2 = body[6]
                vraag3 = body[8]
                datum = body[10]
                #print(naam)
                #print(vraag1)
                #print(vraag2)
                #print(vraag3)
                #print(datum)
                # insert values in database
                cur.execute("INSERT INTO %s (%s) VALUES ('%s', '%s', '%s', '%s',timestamp '%s');" %(table_db2, table_values2, naam, vraag1, vraag2, vraag3, datum))
                #print("inserted")
                # commit the action
                conn.commit()
            except:
                print("\tSomething went wrong")
#print("\n")
# set all the read mails in map destination (copy to map, store in bin)
if len(msg_ids) > 0:
    mail.copy(msg_ids, destination2)
    mail.store(msg_ids, '+FLAGS', r'(\Deleted)')



# close cursor and connection to database
cur.close()
conn.close()
# close connection to mailserver
mail.close()
mail.logout()

# see if something was printed
input('Press enter to quit')