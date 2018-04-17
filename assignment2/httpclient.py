#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

# Modified by: Brett Garbitt 
# Date: 2018-02-14
# CCID: bgarbitt
# Class: CMPUT 296
import sys
import socket
import re
from time import gmtime, strftime # For current date in GMT (google UTC)
from urllib.parse import urlsplit, parse_qs, unquote

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        #return None

    def get_code(self, data):
        response = data.split(" ")
        return response[1]

    def get_headers(self,data):
        response = data.split("\r\n")
        headers  = ""
        for header in response[1:]:
            if not header:
                break
            else:
                headers += header+"\r\n"
        return headers

    def get_body(self, data):
        response = data.split("\r\n\r\n")
        body = ''.join(response[1:])
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    # Retrieve information from URI
    def GET(self, url, args=None):
        '''
        The idea, I believe, is to convert a URI into a format that web servers
        can easily interpret so they can respond with what we request. Convert a
        URI to the form:

        Request-Line
        *(( general-header | request-header | entity-header ) \r\n)
        \r\n
        [ message-body ] <--- I don't think this is used in a GET request.

        If the server interprets this request properly, they will send a response 
        message that we can take and interpret (usually to display a website on 
        the browser).
        '''
        re_code = 500
        body = ""
        u_scheme, u_host, u_port, u_path, u_query, u_fragment = self.parse(url);

        if (u_port is None) and (u_scheme.lower() == "http"):
            u_port = '80'
        elif (u_port is None) and (u_scheme.lower() == "https"):
            u_port = '443'

        query = ''
        if u_query:
            for key in u_query:
                for value in u_query[key]:
                    query+="&"+key+"="+value
        if args is not None:
            for key in args:
                for value in args[key]:
                    if value:
                        query+="&"+key+"="+value
        if query:
            query = "?" + query[1:]

        # Connecting to server
        self.connect(u_host, int(u_port))

        # Preparing request message
        # Format should be:
        #   Request-Line\r\n
        #   *(( general-header | request-header | entity-header )\r\n)
        #   \r\n
        #   [ message-body ]  <---- Not recommended for GET.
        # --------------------------
        # Request-Line
        request_line = "GET /" \
                        + '/'.join(u_path) \
                        + query \
                        + " HTTP/1.1\r\n"
        # Headers
        headers = self.build_headers(u_host, len(body.encode("utf-8")))
        # Message Body (= entity-body) (Not recommended for GET)

        # Combining to make the request message (ignoring message body)
        request = request_line + headers + "\r\n"
        
        # Error handling
        if (u_scheme != "http"):
            return None

        self.sendall(request)
        response = self.recvall(self.socket)
        
        # Retrieving important response information
        re_head = ""
        try:
            re_code = self.get_code(response)
            re_head = self.get_headers(response)
            re_body = self.get_body(response)
        except:
            print("oh no")

        return HTTPResponse(int(re_code), re_body)

    # Post data, append data, change data
    def POST(self, url, args=None):
        '''
        The idea, I believe, is to convert a URI into a format that web servers
        can easily interpret so they can respond with what we request. Convert a
        URI to the form:

        Request-Line
        *(( general-header | request-header | entity-header ) \r\n)
        \r\n
        [ message-body ]

        If the server interprets this request properly, they will send a response 
        message that we can take and interpret (usually to display a website on 
        the browser).
        '''
        
        re_code = 500
        body = ""
        u_scheme, u_host, u_port, u_path, u_query, u_fragment = self.parse(url);
        
        if (u_port is None) and (u_scheme.lower() == "http"):
            u_port = '80'
        elif (u_port is None) and (u_scheme.lower() == "https"):
            u_port = '443'

        query = ''
        if u_query:
            for key in u_query:
                for value in u_query[key]:
                    query+="&"+key+"="+value
        if args is not None:
            for key in args:
                query+="&"+key+"="+args[key]
        if query:
            body = query[1:]
            
        # Connecting to server
        self.connect(u_host, int(u_port))

        # Preparing request message
        # Format should be:
        #   Request-Line\r\n
        #   *(( general-header | request-header | entity-header )\r\n)
        #   \r\n
        #   [ message-body ]
        # --------------------------
        # Request-Line
        request_line = "POST /" \
                        + '/'.join(u_path) \
                        + " HTTP/1.1\r\n"
        # Headers
        headers = self.build_headers(u_host, len(body.encode("utf-8")))
        
        if len(body) == 0:
            headers+="Content-Language: en\r\n"+\
                     "Content-Length: 0\r\n"+\
                     "Content-Type: application/x-www-form-urlencoded\r\n"
        
        # Combining to make the request message
        request = request_line + headers + "\r\n" + body
        
        # Error handling (we're only dealing with the http scheme.)
        if (u_scheme != "http"):
            return None
        
        self.sendall(request)
        response = self.recvall(self.socket)
        
        re_body, re_head = "", ""
        try:
            re_code = self.get_code(response)
            re_head = self.get_headers(response)
            re_body = self.get_body(response)
        except:
            print("oh no")

        return HTTPResponse(int(re_code), re_body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

    def parse(self, url):
        parsed = urlsplit(url)
        scheme = parsed.scheme
        host = unquote(parsed.hostname)
        port = parsed.port
        path = parsed.path
        query = parsed.query
        fragment = unquote(parsed.fragment)
        if fragment == '':
            fragment = None
        query = parse_qs(query)
        path = list(map(unquote, path.split('/')))[1:]
        return (scheme, host, port, path, query, fragment)

    def build_headers (self, host, body_l):
        headers = {'general': {}, 'request': {}, 'entity': {}}

        general = ''
        request = ''
        entity = ''

        # General Headers (Cache-Control, Connection, Date, Pragma, Trailer,
        #                  Transfer-Encoding, Upgrade, Via, Warning)
        # http/1.1 default
        headers['general']['cache_control'] = "Cache-Control: private\r\n"
        # http/1.1 default
        headers['general']['connection'] = "Connection: close\r\n"
        # date of request creation
        headers['general']['date'] = "Date: " + \
                                     strftime("%a, %d %b %Y %H:%M:%S", gmtime()) + \
                                     " GMT\r\n"
        # used to help prevent caching.
        headers['general']['pragma'] = None
        # sends metadata, such as 'Expire'.
        headers['general']['trailer'] = None
        # no encoding done.
        #headers['general']['transfer_encoding'] = "Transfer-Encoding: identity\r\n"
        # used to switch to preferred protocols if available.
        headers['general']['upgrade'] = None
        # used for proxies/gateways.
        headers['general']['via'] = None
        # used if wanting to warn about possible semantics.
        headers['general']['warning'] = None
        # creating the general header
        for header in headers['general']:
            if headers['general'][header] is not None:
                general += headers['general'][header]

        # Request Headers (Accept, A-Charset, A-Encoding, A-Language, Authorization,
        #                  Expect, From, Host, If-Match, If-Modified-Since,
        #                  If-None-Match, If-Range, If-Unmodified-Since, Max-Forwards,
        #                  Proxy-Authorization, Range, Referer, TE, User-Agent)
        # acceptable media types
        headers['request']['accept'] = "Accept: */*\r\n"
        # acceptable charset
        headers['request']['accept_charset'] = "Accept-Charset: utf-8, iso-8859-1;q=0.5\r\n"
        # accept any server encoding response.
        headers['request']['accept_encoding'] = "Accept-Encoding: *\r\n"
        # acceptable language for a response.
        headers['request']['accept_language'] = "Accept-Language: en;q=0.8, en-gb;q=0.7\r\n"
        # used to autheticate a user to a server.
        headers['request']['authorization'] = None
        # used to get confirmation from server to send large body.
        headers['request']['expect'] = None
        # send email address with request, possibly for logging purposes.
        headers['request']['_from'] = None
        # host supplied in URI
        headers['request']['_host'] = "Host: " + host + "\r\n"
        # condition to allow efficient updates of cache information.
        headers['request']['if_match'] = None
        # if entity modified since date, send response, else, 304.
        headers['request']['if_modified_since'] = None
        # condition to allow efficient updates of cache information.
        headers['request']['if_none_match'] = None
        # if entity has changed, send me full entity, else, send missing content.
        headers['request']['if_range'] = None
        # if entity not modified since date, send response, else, 412.
        headers['request']['if_unmodified_since'] = None
        # used for proxies/gateways.
        headers['request']['max_forwards'] = None
        # used for proxies/gateways.
        headers['request']['proxy_authorization'] = None
        # only want what's in this range (or ranges).
        headers['request']['_range'] = None
        # allows reference for content being sent to server (for server benefit).
        headers['request']['referer'] = None
        # can specify type of transfer coding's are acceptable in the response.
        headers['request']['te']= None
        # can specify user information for statistics and tailored responses.
        headers['request']['user_agent'] = None
        # creating the request header
        for header in headers['request']:
            if headers['request'][header] is not None:
                request += headers['request'][header]

        # Entity Headers (Allow, Content-Encoding, C-Language, C-Length, C-Location,
        #                 C-MD5, C-Range, C-Type, Expires, Lst-Modified, extension-h)
        # list of allowed methods (GET, PUT), returns 405 if server doesn't have it.
        headers['entity']['allow'] = None
        # tells server what encodings have been used on entity.
        headers['entity']['content_encoding'] = None
        # length of body in OCTETS (8 bits) and language of body.
        if (int(body_l) > 0):
            headers['entity']['content_language'] = "Content-Language: en\r\n"
            headers['entity']['content_length'] = "Content-Length: " + \
                                                  str(body_l) + \
                                                  "\r\n"
            headers['entity']['content_type'] = "Content-Type: application/x-www-form-urlencoded\r\n"
        else:
            headers['entity']['content_language'] = None
            headers['entity']['content_length'] = None
            headers['entity']['content_type'] = None
            
        # used to supply location of entity when it's accessible to server.
        headers['entity']['content_location']= None
        # apparently removed in 2014.
        headers['entity']['content_md5'] = None
        # where in the full body message a partial message belongs.
        headers['entity']['content_range'] = None
        # date/time which response is considered stale.
        headers['entity']['expires'] = None
        # date/time which server believes entity was last modified?
        headers['entity']['last_modified'] = None
        # custom headers some servers may want.
        headers['entity']['extension_header']= None
        # creating the entity header
        for header in headers['entity']:
            if headers['entity'][header] is not None:
                entity += headers['entity'][header]

        # request headers
        req_hed = ''
        
        # combining the headers if they exist
        if general != '':
            req_hed += general
        if request != '':
            req_hed += request
        if entity != '':
            req_hed += entity

        # returning the headers if there are any, else return None.
        if req_hed == '':
            return None
        else:
            return req_hed

    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
