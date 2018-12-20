import socket
import asyncio
import random
import sqlite3

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

async def server(loop):
	host = ''
	port = 10000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		s.bind((host,port))
		s.setblocking(False)
		print("server started...")
	except socket.error as e:
		print(str(e))

	s.listen()
	print ("listening on port:",s.getsockname()[1])
	while True:
		conn , addr = await loop.sock_accept(s)
		print('connected to:' +addr[0] +":"+str(addr[1]))

		id = random.randint(1,9999999999)
		loop.create_task(client_thread(conn,id, loop))
	
		connections.update({id:conn})
		print(connections)
		
async def client_thread(conn, id, loop):
	await loop.sock_sendall(conn, b'connected...\nenter a username: ')
	(username,f) = ('',0)
	while True:
		data = await loop.sock_recv(conn, 1024)
		data=data.decode('utf-8')
		if f==0: 
			if data != '':
				print(data)
				username = data
				db_up_del('add',id,username)
				await loop.sock_sendall(conn, b'updated\n')
			f=1	
		if data == 'list':
			await loop.sock_sendall(conn, str.encode(str(db_list())+"\n"))	
		if not data:
			connections.pop(id)
			db_up_del('del',id)
			conn.close()
			break
	conn.close()	
		
if __name__=='__main__':
	connections = {}
	loop=asyncio.get_event_loop()
	loop.run_until_complete(server(loop))
