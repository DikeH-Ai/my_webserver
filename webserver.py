#!/usr/bin/python3

# import socket
import socket

# setup web server function
def server_func():
	# set host and port values
	host = ''
	port = 11172
	try:
		# instantiate socket object
		webserver = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

		# bind socket object to hardware
		webserver.bind((host,port))

		# listen for connections to socket
		webserver.listen()

		# approve connections
		clientserver, clientaddr = webserver.accept()
		print(f"Connected to {clientaddr[0]}:{clientaddr[1]}")

		# get request data
		data = clientserver.recv(2048).decode('utf-8')

		if data:
			print(data)
			request_to_dict(data)

	except Exception as e:
		print(f"Error: {str(e)}")
	finally:
		webserver.close()

# setup request handler
def request_to_dict(data: str) -> dict:
	# convert request data to dict for easy access and manipulation
	data_dict = {}
	# split per line 
	per_line = data.split("\n")
	# split request line data 
	request_line = per_line[0].split(" ")
	request_dict = {value: request_line[idx] for idx, value in enumerate(["method", "path", "version"]) if request_line[idx]}
	# append to data_dict
	data_dict.update(request_dict)

	# get for header
	header = per_line[1:]
	if data_dict["method"] not in ["POST", "PATCH", "PUT"]:
		# without body
		header_dict = {value[0]:value[1].strip() for x in header if (value := x.split(":")) and (len(value) == 2)}
		data_dict.update(header_dict)
	else:
		# with body
		
		pass
	return data_dict
if __name__ == "__main__":
	server_func()
