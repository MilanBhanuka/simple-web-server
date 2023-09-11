# Python Web Server README

This README file provides instructions for setting up and running a basic Python-based web server capable of serving PHP and static files.

## Prerequisites

Before you begin, ensure you have the following software installed on your system:

- Python: [Download and Install Python](https://www.python.org/downloads/)
- PHP (optional): [Download and Install PHP](https://www.php.net/downloads.php)


## Configuration

Open the webserver.py file and adjust the following variables as needed:

base: The directory where your web server will serve files from (default is "htdocs").
host: The host or IP address on which your server will listen (default is "127.0.0.1").
port: The port on which your server will listen (default is 2728).
If you plan to use PHP, ensure you have PHP installed and set the php_path variable in the webserver.py file to the correct PHP executable path.

## Running the Server

To start the web server, run the "python server.py" command
The server will now be running on the specified host and port (e.g., http://127.0.0.1:2728).


## Serving PHP Files

Place your PHP files in the "htdocs" directory.

Access PHP files through your web browser (e.g., http://localhost:2728/yourfile.php).
