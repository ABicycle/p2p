import socket
from thread import *
import random
import sqlite3


host = ''
port = 10000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = {}

try:
	s.bind((host,port))
	print "server started..."
except socket.error as e:
	print(str(e))

s.listen(5)
print ("listening on port:",s.getsockname()[1])


def db_up_del(op,id,username=""):
	conn = sqlite3.connect('users.db')
	c = conn.cursor()

	if op == 'add':
		c.execute("INSERT INTO users (id, username) values (?, ?)",(id, username))
	elif op == 'del':
		c.execute("DELETE FROM users WHERE id=?", (id,))

	conn.commit()
	conn.close()


def db_list():
	conn = sqlite3.connect('users.db')
	c = conn.cursor()

	c.execute("SELECT * FROM users")
	return(c.fetchall())

	conn.close()


def client_thread(conn,id):
	conn.send('connected...\nenter a username: ')
	(username,f) = ('',0)
	while True:
		data = conn.recv(1024).rstrip("\n\r")

		if f==0: 
			if data != '':
				print data
				username = data
				db_up_del('add',id,username)
				conn.send("updated\n")
			f=1


		if data == 'list':
			conn.send(str(db_list())+"\n")
				
		if not data:
			connections.pop(id)
			db_up_del('del',id)
			conn.close()
			break
	conn.close()	

while True:
	conn , addr = s.accept()
	print('connected to:' +addr[0] +":"+str(addr[1]))

	id = random.randint(1,9999999999)
	start_new_thread(client_thread,(conn,id))
	
	connections.update({id:conn})
	print connections
