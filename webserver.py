#!/usr/bin/python3

import socket

def main():
	try:
		# main server function
		host = ''
		port = 15000

		# creates and returns a webserver
		sock = tcp_socket_server(host, port)

		# accept the connection
		accept_connection(sock)

	except Exception as e:
		print(f"str{e}")
	finally:
		sock.close()

# setup tcp socket
def tcp_socket_server(host, port):
	# instantiate socket object
	webserver = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

	# bind socket object to hardware
	webserver.bind((host, port))

	# listen for connections to socket
	webserver.listen()

	# return webserver object
	return webserver

# handle clients
def accept_connection(webserver): 
	while True:
		# approve connections
		clientserver, clientaddr = webserver.accept()
		print(f"Connected to {clientaddr[0]}:{clientaddr[1]}")

		client_request_handler(clientserver, clientaddr)

		# close client server
		clientserver.close()

# handles data from the client
def client_request_handler(clientserver, clientaddr):
	while True:
        # get request data
		data = clientserver.recv(2048).decode('utf-8')

		if data:
		    # convert data to dictionary
			data_dict = request_to_dict(data)

		    # get response
			response = handle_http_method(data_dict)

		    # send the response
			clientserver.sendall(response)
		if data_dict.get("Connection", "").lower() != "keep-alive":
			break

# convert request data to dict
def request_to_dict(data: str) -> dict:
	data_dict = {}

	# split per line
	per_line = data.split("\n")

	# split request line data
	request_line = per_line[0].split(" ")
	request_dict = {value: request_line[idx] for idx, value in enumerate(
	["method", "path", "version"]) if request_line[idx]}
	data_dict.update(request_dict)

	if data_dict["method"] not in ["POST", "PATCH", "PUT"]:
		# get form header
		header = per_line[1:]
		header_dict = {value[0]: value[1].strip() for x in header if (
		value := x.split(":")) and (len(value) == 2)}
		data_dict.update(header_dict)
	else:
		# with body
		header, body = data.split("\n\n", 1)
		data_dict["body"] = body
		print(data_dict)

	return data_dict

def handle_http_method(data_dict):
	# handle request methods
	method_dict = {
		"GET": get_handler
	}

	if data_dict["method"] in method_dict:
		return method_dict[str(data_dict["method"])](data_dict)
	else:
		with open("./status_template/405.html", "rb") as file:
			content = file.read()
			response = response_builder(statuscode=405, content=content, contenttype=get_content_type(data_dict["path"]))
		return response

# HTTP methods
def get_handler(data_dict):
	# handle get method
	path = data_dict["path"]

	if path == "/":
		path = "/index.html"

	try:
		path = "./www" + path
		with open(path, "rb") as file:
			content = file.read()
		response = response_builder(statuscode=200, content=content, contenttype=get_content_type(path))
	except Exception as e:
		with open("./status_template/404.html", "rb") as file:
			content = file.read()
		response = response_builder(statuscode=404, content=content, contenttype=get_content_type(path))
	finally:
		return response

def put_handler():
	pass

def del_handler():
	pass

def post_handler():
	pass

def response_builder(statuscode, contenttype, content):
	# construct response
	HTTP_STATUS_CODES = {
	    100: "Continue",
	    101: "Switching Protocols",
	    102: "Processing",
	    103: "Early Hints",
	    200: "OK",
	    201: "Created",
	    202: "Accepted",
	    203: "Non-Authoritative Information",
	    204: "No Content",
	    205: "Reset Content",
	    206: "Partial Content",
	    207: "Multi-Status",
	    208: "Already Reported",
	    226: "IM Used",
	    300: "Multiple Choices",
	    301: "Moved Permanently",
	    302: "Found",
	    303: "See Other",
	    304: "Not Modified",
	    305: "Use Proxy",
	    307: "Temporary Redirect",
	    308: "Permanent Redirect",
	    400: "Bad Request",
	    401: "Unauthorized",
	    402: "Payment Required",
	    403: "Forbidden",
	    404: "Not Found",
	    405: "Method Not Allowed",
	    406: "Not Acceptable",
	    407: "Proxy Authentication Required",
	    408: "Request Timeout",
	    409: "Conflict",
	    410: "Gone",
	    411: "Length Required",
	    412: "Precondition Failed",
	    413: "Payload Too Large",
	    414: "URI Too Long",
	    415: "Unsupported Media Type",
	    416: "Range Not Satisfiable",
	    417: "Expectation Failed",
	    418: "I'm a teapot ☕",
	    421: "Misdirected Request",
	    422: "Unprocessable Entity",
	    423: "Locked",
	    424: "Failed Dependency",
	    425: "Too Early",
	    426: "Upgrade Required",
	    428: "Precondition Required",
	    429: "Too Many Requests",
	    431: "Request Header Fields Too Large",
	    451: "Unavailable For Legal Reasons",
	    500: "Internal Server Error",
	    501: "Not Implemented",
	    502: "Bad Gateway",
	    503: "Service Unavailable",
	    504: "Gateway Timeout",
	    505: "HTTP Version Not Supported",
	    506: "Variant Also Negotiates",
	    507: "Insufficient Storage",
	    508: "Loop Detected",
	    510: "Not Extended",
	    511: "Network Authentication Required",
	}

	status_text = HTTP_STATUS_CODES.get(statuscode, "Unknown Status")

	response_header = (
		f"HTTP/1.1 {statuscode} {status_text}\r\n"
		f"Content-Type: {contenttype}\r\n"
		f"Content-Length: {len(content)}\r\n"
		"\r\n"
	)

	return response_header.encode() + content

def get_content_type(file_path):
	# get mime type
	import mimetypes
	content_type, _ = mimetypes.guess_type(file_path)
	return str(content_type) or "application/octet-stream"

if __name__ == "__main__":
	main()

