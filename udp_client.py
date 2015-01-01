#!/usr/bin/env python
import socket, sys


class UDPclient():

	def udp_send(self, server, port, msg):
		client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		client.sendto(msg,(server,port))
		response, addr = client.recvfrom(4096)
		print response


if __name__ == '__main__':
	try:
		server = sys.argv[1]
		port = sys.argv[2]
		msg = sys.argv[3]
		port = int(port, 0)
		#Can hardcode options as well # msg = ""
		client = UDPclient()
		client.udp_send(server, port, msg)
	except IndexError:
		print('Usage: udp_client.py <server> <port> <message>')
		sys.exit(1)
