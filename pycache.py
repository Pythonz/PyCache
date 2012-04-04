#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import socket
from thread import start_new_thread
from sys import exit
from time import sleep
from ConfigParser import RawConfigParser

__version__ = open("version", "r").read()

class PyCache:
	def __init__(self):
		try:
			Config = RawConfigParser()
			Config.read("config.cfg")
			self.socket = socket()
			self.socket.bind((Config.get("listen", "ip"), Config.getint("listen", "port")))
			self.socket.listen(Config.getint("listen", "limit"))
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
				line = client.recv(int(maxbuf)).rstrip()
				if not line:
					del cache
					client.close()
					print("DISCONNECT: " + address[0] + ":" + str(address[1]))
				if len(line.split()) == 1:
					if line.upper() == "QUIT":
						del cache
						client.send("OK\n")
						client.close()
						print("DISCONNECT: " + address[0] + ":" + str(address[1]))
					elif line.upper() == "DELE":
						del cache
						cache = dict()
						client.send("OK\n")
					elif line.upper() == "CONN":
						client.send("OK\n")
					else:
						client.send("ERROR\n")
				if len(line.split()) == 2:
					command = line.split()[0].upper()
					string = line.split()[1].lower()
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
					elif command == "EXIS":
						if cache.has_key(string):
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
					command = line.split()[0].upper()
					string = line.split()[1].lower()
					data = ' '.join(line.split()[2:])
					if command == "STOR":
						cache[string] = data
						client.send("OK\n")
					elif command == "RENA":
						if cache.has_key(string):
							cache[data.split()[0].lower()] = cache[string]
							del cache[string]
							client.send("OK\n")
						else:
							client.send("ERROR\n")
					else:
						client.send("ERROR\n")
		except Exception:
			pass
		except KeyboardInterrupt:
			exit("Abort ...")
		finally:
			return 1

while True:
	print("Started PyCache " + __version__)
	PyCache()
	print("Stopped PyCache " + __version__)
	sleep(5)
