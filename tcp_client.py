#!/usr/bin/env python
import socket, sys


class TCPclient():

	def tcp_send(self, server, port, msg):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((server,port))
		client.send(msg)
		response = client.recv(4096)
		print response


if __name__ == '__main__':
	try:
		server = sys.argv[1]
		port = sys.argv[2]
		msg = sys.argv[3]
		port = int(port, 0)
		#Can hardcode options as well # msg = "HEAD / HTTP/1.1\r\nHost: shadowcats.info\r\n\r\n"
		client = TCPclient()
		client.tcp_send(server, port, msg)
	except IndexError:
		print('Usage: tcp_client.py <server> <port> <message>')
		sys.exit(1)
