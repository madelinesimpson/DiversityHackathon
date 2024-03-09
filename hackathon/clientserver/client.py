import socket
import threading
import sys 


#TODO: Implement a client that connects to your server to chat with other clients here
# Use sys.stdout.flush() after print statemtents
import argparse
close = False

def start_client(host, port, username, passcode):
	global close
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((host, port))
	client_socket.send(bytes(f"{username}*{passcode}*{host}", 'utf-8'))
	threading.Thread(target=receive_messages, args=(client_socket,)).start()
	while True:
		try:
			message = input()
			threading.Thread(target=send_message, args=(client_socket, message,)).start()
			if message == ":Exit":
				close = True
				client_socket.close()
				break
		except EOFError:
			pass

def receive_messages(client_socket):
	global close
	while not close:
		try:
			server_message = client_socket.recv(1024).decode()
			print(server_message)
			sys.stdout.flush()
			if server_message == "Incorrect passcode":
				break
		except OSError as e:
			if e.errno == 9:
				break
			else:
				raise e

def send_message(client_socket, input):
	client_socket.send(input.encode())

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-join", action="store_true")
	parser.add_argument("-host", dest='host', type=str)
	parser.add_argument("-port", dest='port', type=int)
	parser.add_argument("-username", dest='username', type=str)
	parser.add_argument("-passcode", dest='passcode', type=str)
	args = parser.parse_args()
	start_client(args.host, args.port, args.username, args.passcode)
