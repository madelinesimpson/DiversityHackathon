import socket
import threading
import sys 


#TODO: Implement all code for your server here
# Use sys.stdout.flush() after print statemtents

import argparse
import datetime

host = "127.0.0.1"
clients = {}

def handle_clients(client_socket, username):
	while True:
		client_message = client_socket.recv(1024).decode()
		if client_message == ":Exit":
			print(f"{username} left the chatroom")
			sys.stdout.flush()
			client_socket.close()
			clients.pop(username)
			for client in clients:
				threading.Thread(target=send_message, args=(client, f"{username} left the chatroom",)).start()
			break
		elif client_message.startswith(":dm"):
			_, receiver, _ = client_message.split(" ", 2) 
			message = client_message[5 + len(receiver):]
			print(f"{username} to {receiver}: {message}")
			sys.stdout.flush()
			threading.Thread(target=send_message, args=(receiver, f"{username}: {message}",)).start()
		else:
			if client_message == ":)":
				client_message = "[feeling happy]"
			if client_message == ":(":
				client_message = "[feeling sad]"
			if client_message == ":mytime":
				client_message = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
			if client_message == ":+1hr":
				client_message = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%a %b %d %H:%M:%S %Y")
			print(f"{username}: {client_message}")
			sys.stdout.flush()
			for client in clients:
				if client != username:
					threading.Thread(target=send_message, args=(client, f"{username}: {client_message}",)).start()

def send_message(username, message):
	clients.get(username).send(message.encode())

def start_server(port, passcode):
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((host, port))
	server_socket.listen()
	print(f"Server started on port {port}. Accepting connections")
	sys.stdout.flush()

	while True:
		conn, _ = server_socket.accept()
		credentials = conn.recv(1024).decode()
		cred = credentials.split("*")
		client_username = cred[0]
		client_passcode = cred[1]
		client_host = cred[2]
		if client_passcode != passcode:
			conn.send(f"Incorrect passcode".encode())
			conn.close()
		else:
			clients[client_username] = conn
			threading.Thread(target=handle_clients, args=(conn, client_username,)).start()
			threading.Thread(target=send_message, args=(client_username, f"Connected to {client_host} on port {port}",)).start()
			for client in clients:
				if client != client_username:
					threading.Thread(target=send_message, args=(client, f"{client_username} joined the chatroom",)).start()
			print(f"{client_username} joined the chatroom")
			sys.stdout.flush()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-start", action="store_true")
	parser.add_argument("-port", dest='port', type=int)
	parser.add_argument("-passcode", dest='passcode', type=str)
	args = parser.parse_args()
	start_server(args.port, args.passcode)