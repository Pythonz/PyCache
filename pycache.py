#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import socket
from thread import start_new_thread
from sys import exit
from time import sleep

class PyCache:
	def __init__(self):
		try:
			self.socket = socket()
			self.socket.bind(("127.0.0.1", 1270))
			self.socket.listen(1024)
			while True:
				client, address = self.socket.accept()
				start_new_thread(self.cache, (client, address))
				print("CONNECT: " + address[0] + ":" + str(address[1]))
		except Exception:
			pass
		except KeyboardInterrupt:
			exit("Abort ...")
		finally:
			return None

	def cache(self, client, address):
		try:
			cache = dict()
			maxbuf = 2048
			while True:
				line = client.recv(2048).rstrip()
				if not line:
					del cache
					client.close()
					print("DISCONNECT: " + address[0] + ":" + str(address[1]))
				if len(line.split()) == 1:
					if line == "QUIT":
						del cache
						client.send("OK\n")
						client.close()
						print("DISCONNECT: " + address[0] + ":" + str(address[1]))
					else:
						client.send("ERROR\n")
				if len(line.split()) == 2:
					command = line.split()[0]
					string = line.split()[1]
					if command == "RETR":
						if cache.has_key(string):
							client.send("SEND " + string + " " + cache[string] + "\n")
						else:
							client.send("ERROR\n")
					elif command == "DROP":
						if cache.has_key(string):
							del cache[string]
							client.send("OK\n")
						else:
							client.send("ERROR\n")
					elif command == "LINE":
						if string.isnum():
							maxbuf = int(string)
							client.send("OK\n")
						else:
							client.send("ERROR\n")
					else:
						client.send("ERROR\n")
				if len(line.split()) > 2:
					command = line.split()[0]
					string = line.split()[1]
					data = ' '.join(line.split()[2:])
					if command == "STOR":
						cache[string] = data
						client.send("OK\n")
					else:
						client.send("ERROR\n")
		except Exception:
			pass
		except KeyboardInterrupt:
			exit("Abort ...")
		finally:
			return 1

while True:
	print("Started PyCache")
	PyCache()
	print("Stopped PyCache")
	sleep(5)
