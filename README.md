# Minimal Python Web Server

This project is a minimalist Python-based TCP web server designed to serve static files and handle basic HTTP GET requests. It aims to deepen my understanding of how web servers work under the hood by building one from scratch using Python's `socket` library.

## Project Aim

The primary goal of this project is to demonstrate how a basic web server handles HTTP requests, parses them manually, and responds with appropriate HTML content. It serves as a learning tool for understanding network programming, HTTP protocols, and server-client architecture.

## Features

- Basic TCP socket server using Python’s `socket` module
- Accepts client connections and handles requests
- Parses raw HTTP requests into structured dictionaries
- Serves static files (HTML, CSS, JS) from a `www/` directory
- Custom 404 and 405 error pages from `status_template/`
- Handles `GET` requests (other methods like `POST`, `PUT`, `DELETE` are stubbed)

## Directory Structure

```
project-root/
│
├── www/                 # Public directory for served content (e.g., index.html)
├── status_template/     # Error templates (e.g., 404.html, 405.html)
├── server.py            # Main server script (provided code)
└── README.md            # Project documentation
```

## Usage

1. **Prepare Your Environment**  
   Make sure Python 3 is installed on your system.

2. **Create Necessary Files**  
   - Add `index.html` in the `www/` directory.
   - Add `404.html` and `405.html` in the `status_template/` directory.

3. **Run the Server**  
   From your terminal:
   ```bash
   python3 server.py
   ```

4. **Access the Server**  
   Open a browser and go to:  
   ```
   http://localhost:15000/
   ```

## Notes

- The server listens on port `15000` by default.
- All requests are handled synchronously.
- Only `GET` requests are supported at this time.
- The `Connection: keep-alive` header is supported for persistent connections.

## Future Improvements

- Add support for `POST`, `PUT`, `DELETE` methods
- Implement multithreading or async handling for concurrent clients
- Add logging and better error handling