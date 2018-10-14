# p2p
This repository is focused on creating a <b>peer-to-peer chat application</b> using Python.

## getting started
After cloning the file `server.py` create a sqlite data base with the name of `users.db` in the same folder.<br> 
Now, navigate to the directory and run the application by `python server.py` (don't run the application from a different folder by referring the path to that file)<br>
This will start the server. It is now listening to the same IP address of your computer on port 10000.<br>
Once you are done with this, you can now communicate with the server by TCP connection. 
To do so open-up a new terninal and type `telnet YOUR-SERVER-IP 10000`.<br>
Done! now it's connected. You can do it for multiple terminals (clients) to get connected with the server.

## work
* Once done with the connection. It will ask for a name to the client to log it into the data base.
* Now if the client types `list`, it will show the list of all the existing clients connected to the server.
