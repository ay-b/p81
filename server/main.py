import os
import sys
import http.server
import socketserver
import socket
import jinja2
import requests
import json

# Configs
LISTENING_PORT       = os.environ.get('LISTENING_PORT')     or 8000
LISTENING_ADDRESS    = os.environ.get('LISTENING_ADDRESS')  or '127.0.0.1'
ECHO_DATA            = os.environ.get('ECHO_DATA')
HTML_DIR             = os.environ.get('HTML_DIR')           or './'
HTML_INDEX_FILE      = os.environ.get('HTML_INDEX_FILE')    or 'index.html'
JINJA_OUTPUT         = os.environ.get('JINJA_OUTPUT')       or 'default_response.html'
JINJA_TEMPLATE       = os.environ.get('JINJA_TEMPLATE')     or 'default_template.html'
# /Configs


# Initial checks
if not os.environ.get('ECHO_DATA'):
    print("FATAL: ECHO_DATA variable is not set.", file=sys.stderr)
    exit(1)

def port_check(HOST, PORT):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.settimeout(2) #Timeout 2 sec
   try:
      s.connect((HOST, PORT))
      return True
   except:
      return False

if not port_check(LISTENING_ADDRESS, LISTENING_PORT):
   print("Port test ok.")
else:
   err = "FATAL: Port "+LISTENING_ADDRESS+":"+str(LISTENING_PORT)+" is occupied"
   print(err, file=sys.stderr)
   exit(1)
# /Initial checks

# This thing has rate limits and try/catch for that isn't implemented. 
# Therefore, if location fields are empty — rate limit reached and URL returns json with error which isn't parsed the right way.
def get_ip_location(ip):
   response = requests.get(f'https://ipapi.co/{ip}/json/').json()
   location_data = {
      "ip": ip,
      "city": response.get("city"),
      "region": response.get("region"),
      "country": response.get("country_name")
   }
   return location_data

# Writing response to file
# *It's a bad idea to write to file each request but I don't want to bother about serving HTML from memory now*
def gen_resp(data):
   print(data, file=sys.stdout)
   # generate_response = jinja2.Environment(loader=jinja2.FileSystemLoader(HTML_DIR)).get_template(JINJA_TEMPLATE).render(CLIENT_IP=ip)
   generate_response = jinja2.Environment(loader=jinja2.FileSystemLoader("./")).get_template("default_template.html").render(
      ECHO_DATA   =ECHO_DATA,
      CLIENT_IP   =data['ip'],
      CITY        =data['city'],
      REGION      =data['region'],
      COUNTRY     =data['country']
   )
   with open(JINJA_OUTPUT,'w') as f: f.write(generate_response)
# /Writing response to file



# Handler = http.server.SimpleHTTPRequestHandler
class Handler(http.server.SimpleHTTPRequestHandler):
   def do_GET(self):
      if self.path == '/':
         self.path = HTML_INDEX_FILE
      else:
         self.path = './default_response.html'
         print("Client:", self.client_address[0])
         gen_resp(get_ip_location(self.client_address[0]))
      return http.server.SimpleHTTPRequestHandler.do_GET(self)


# Main loop
def main():
   with socketserver.TCPServer(("", LISTENING_PORT), Handler) as httpd:
      addr_port = LISTENING_ADDRESS+":"+str(LISTENING_PORT)
      print("Listening at port:", addr_port)
      print("Echoing data is:", ECHO_DATA)
      httpd.serve_forever()


if __name__ == "__main__":
    main()
