from socket import socket

class Cache:
	def __init__(self):
		self.socket = socket()
		self.socket.connect(("127.0.0.1", 1270))
		return None

	def stor(self, string, data):
		self.socket.send("STOR " + string + " " + data + "\n")
		recv = self.socket.recv(10).rstrip()
		if recv == "OK":
			return True
		return False

	def retr(self, string, maxlen=1024):
		self.socket.send("RETR " + string + "\n")
		recv = self.socket.recv(int(maxlen)).rstrip()
		if recv != "ERROR":
			return ' '.join(recv.split()[2:])
		return False

	def drop(self, string):
		self.socket.send("DROP " + string + "\n")
		recv = self.socket.recv(10).rstrip()
		if recv == "OK":
			return True
		return False

	def close(self):
		self.socket.close()
