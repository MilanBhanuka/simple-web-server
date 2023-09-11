import os
import socket
import subprocess

base="htdocs"

def phpObj(data):
      php_string="$data = array(\n"
      for v in data:
            php_string+=f"'{v[0]}'=>'{v[1]}',\n"

      php_string+=");"
      return php_string

def webserver(host,port):
      tempFileLocation = ''
      parameters = ''
      print("Host: ",host)
      print("Port: ",port)

      #create socket
      webSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      print("Socket created.",webSocket)
      #bind socket to port
      webSocket.bind((host,port))
      #listen for connections
      webSocket.listen(5)
      print("Server is running on http://"+host+":"+str(port))

      while True:
            tempFileLocation = ''
            parameters = ''

            #accept connections
            connection,address = webSocket.accept()

            requestLine = connection.recv(4096).decode('utf-8').split("\r\n")
            path = requestLine[0].split(" ")[1]

            if 1<len(path.split("?")):
                  path,parameters = path.split("?")
            
            requestType = requestLine[0].split(" ")[0]

            #get file location
            fileLocation = os.path.join(base,path.lstrip("/"))

            #check whether file exists and is in the base directory
            if os.path.exists(fileLocation) and os.path.commonpath([base,fileLocation]) == base:
                  if os.path.isdir(fileLocation):
                        if os.path.exists(os.path.join(fileLocation,"index.php")):
                              fileLocation = os.path.join(fileLocation,"index.php")
                        elif os.path.exists(os.path.join(fileLocation,"index.html")):
                              fileLocation = os.path.join(fileLocation,"index.html")

                  #check whether file is a php file
                  if os.path.isfile(fileLocation):
                        if fileLocation.endswith(".php"):
                              if requestType == "POST":
                                    postData =  requestLine[requestLine.index("")+1].split("&")
                                    postData = list(map(lambda x:[it for it in x.split("=")],postData))

                                    phpText ="<?php "+phpObj(postData)+" \n $_POST=$data; ?>"

                                    with open(fileLocation,"r") as phpFile:
                                          phpCode = phpFile.read()

                                    directoryPath = os.path.dirname(fileLocation)
                                    fileName = "."+"temp"+os.path.basename(fileLocation)
                                    fileLocation = os.path.join(directoryPath,fileName)
                                    tempFileLocation = fileLocation

                                    with open(fileLocation,"w") as file:
                                          file.write(phpText+phpCode) 

                              if requestType == "GET" and parameters:
                                    getData = parameters.split("&")
                                    getData = list(map(lambda x:[it for it in x.split("=")],getData))

                                    phpText ="<?php "+phpObj(getData)+" \n $_GET=$data; ?>"

                                    with open(fileLocation,"r") as phpFile:
                                          phpCode = phpFile.read()

                                    directoryPath = os.path.dirname(fileLocation)
                                    fileName = "."+"temp"+"_"+os.path.basename(fileLocation)
                                    fileLocation = os.path.join(directoryPath,fileName)
                                    tempFileLocation = fileLocation

                                    with open(fileLocation,"w") as file:
                                          file.write(phpText+phpCode)
                              try:
                                    php_path = r'C:\xampp\php\php.exe'
                                    output = subprocess.run([php_path,fileLocation],shell=True, capture_output=True, text=True, check=True)
                                    response = "HTTP/1.1 2000 OK\r\n\r\n"+output.stdout
                              
                              except subprocess.CalledProcessError as e:
                                    response = "HTTP/1.1 500 Internal Server Error\r\n\r\n"+e.stderr                  
                        else:
                              try:
                                    with open(fileLocation,"rb") as file:
                                          output = file.read()
                                          response = "HTTP/1.1 200 OK\r\n\r\n"+output.decode('utf-8')
                              except Exception as e:
                                    response = "HTTP/1.1 500 Internal Server Error\r\n\r\n"+str(e)
                  else:
                        response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found."
            else:
                  response = "HTTP/1.1 403 Forbidden\r\n\r\nForbidden."
            
            connection.sendall(response.encode('utf-8'))
            connection.close()               
 
host = "127.0.0.1"
port=2728

webserver(host,port)
