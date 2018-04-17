# Weclome to Assignment #1!

# Your name: Brett Garbitt
# The date: 2018-01-21
# The names of any students you consulted with:

# Paste the license you choose for your assignment here.
'''
MIT License

Copyright (c) 2018 Brett Garbitt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
# Instructions: write a URL parser library in Python 3. This file should contain
# function that when called with a URL will return a 6-tuple of information
# about that URL: the scheme (protocol), the host, the port (or None if there
# is no port specified), the path as a list,
# the query arguments as a dictionary of lists,
# and the fragment.

# For example, if the provided URL is 
# http://localhost:8080/cats/cute/index.html?tag=fuzzy&tag=little+pawsies&show=data%26statistics#Statistics
# then your function should return the following Pythong data structure:
(
    'http',
    'localhost',
    8080,
    [
        'cats',
        'cute',
        'index.html',
        ],
    {
        'tag': [
            'fuzzy',
            'little pawsies',
            ],
        'show': [
            'data&statistics',
            ],
        },
    'Statistics'
    )

# Your function must be named parse_url. I've given you some starter code
# below. There is an accompanying file with this assignment called
# free_tests.py which you should run to test your code. It will call your
# function with various URLs and tell you whether your function returns
# the correct information or not.

# When marking your assignment I will use another file, similar to
# free_tests.py that will test your function in the same way, but using
# different URLs. Your mark on this assignment will be the fraction of
# URLs your function parses correctly. 

# If you are not familiar with tuples, dictionaries and lists in Python please,
# familiarize yourself.

# Do not forget to CITE any code you use from the web or other resources.
# YOU ARE NOT ALLOWED TO USE ANY LIBRARIES CAPABLE OF PARSING URLS OR DECODING
# PERCENT-ENCODED DATA. DOING SO WILL RESULT IN A ZERO MARK FOR THIS
# ASSIGNMENT. IF YOU ARE UNSURE WHETHER YOU CAN USE A PARTICULAR LIBRARY
# PLEASE POST ON ECLASS AND ASK. IF YOU DID NOT ASK TO USE A LIBRARY
# AND USE IT ANYWAY YOU MAY RECIEVE A ZERO MARK FOR THIS ASSIGNMENT.

# Submission instructions: Upload your version of
# this file to eClass under Assignment 1.

# Here is some code to get you started:

def parse_url(url):
    scheme, host, port, path, query, fragment = None, None, None, None, None, None
    cc, cp = 0, 0 # character count, checkpoint

    # scheme
    while url[cc] != ":":
        cc+=1
    scheme = url[:cc]
    if cc+1 < len(url):
        if url[cc+1] == "/":
            if url[cc+2] == "/":
                cc += 3 # to skip double slash
                cp = cc
        else:
            cc+=1
            cp=cc
    else:
        return (scheme, None, None, None, None, None)

    # host
    while url[cc] != ":" and url[cc] != "/" and cc < len(url):
        cc+=1
    if cc != cp:
        host = url[cp:cc]
    
    # port (optional)
    if url[cc] == ":":
        cc+=1
        cp = cc
        while url[cc] != "/":
            cc+=1
        port = url[cp:cc]
        try:
            port = int(port)
        except:
            port = port
        cp = cc + 1

    # path (optional)
    if url[cc] == "/":
        path = []
        cc+=1
        cp=cc
        if cc < len(url):
            while url[cc] != "?" and url[cc] != "#" and cc+1 < len(url):
                # always works if there's an end slash
                if url[cc] == "/":
                    path.append(url[cp:cc])
                    cp = cc + 1
                cc+=1
            # in case there's no end slash
            if cc != cp:
                if cc+1 == len(url):
                    path.append(url[cp:cc+1])
                else:
                    path.append(url[cp:cc])
        else:
            cc-=1
            path.append('')
    # query (optional)
    if url[cc] == "?":
        query = dict()
        cc+=1
        cp = cc
        while url[cc] != "#" and cc+1 < len(url):
            if url[cc] == "=":
                key = url[cp:cc]
                cc+=1
                cp = cc
                if url[cc] == "&":
                    cc+=1
                    cp = cc
            elif url[cc] == "&":
                value = url[cp:cc]
                value = value.replace("+", " ")
                cc+=1
                cp = cc
                if key in query:
                    query[key].append(value)
                else:
                    query[key] = [value]
            else:
                cc+=1
        if url[cc] == "#":
            value = url[cp:cc]
            value = value.replace("+", " ")
            if key in query:
                query[key].append(value)
            else:
                query[key] = [value]
        if cc+1 == len(url):
            value = url[cp:cc+1]
            value = value.replace("+", " ")
            if key in query:
                query[key].append(value)
            else:
                query[key] = [value]

    # Fragment
    if url[cc] == "#":
        cc+=1
        fragment = url[cc:]

    # Always have an empty list and dictionary for HTTP/HTTPS URLS
    if path is None:
        path = ['']
    elif not path:
        path.append('')
    if query is None:
        query = {}
    scheme = decode(scheme)
    host = decode(host)
    port = decode(port)
    for x in range(len(path)):
        path[x] = decode(path[x])
    for keys in query:
        new_key = decode(keys)
        query[new_key] = query.pop(keys)
        for x in range(len(query[new_key])):
            #print(query[new_key][x])
            query[new_key][x] = decode(query[new_key][x])
    fragment = decode(fragment)

    return (
        scheme,
        host,
        port,
        path,
        query,
        fragment
    )

def decode(code):
    if code is None:
        return code

    if isinstance(code, int):
        return code

    library = {"%20":" ", "%21":"!", "%22":"\"", "%23":"#", "%24":"$", \
    "%25":"%", "%26":"&", "%27":"\'", "%28":"(", "%29":")", "%2A":"*", \
    "%2B":"+", "%2C":",", "%2D":"-", "%2E":".", "%2F":"/", "%30":"0", \
    "%31":"1", "%32":"2", "%33":"3", "%34":"4", "%35":"5", "%36":"6", \
    "%37":"7", "%38":"8", "%39":"9", "%3A":":", "%3B":";", "%3C":"<", \
    "%3D":"=", "%3E":">", "%3F":"?", "%40":"@", "%41":"A", "%42":"B", \
    "%43":"C", "%44":"D", "%45":"E", "%46":"F", "%47":"G", "%48":"H", \
    "%49":"I", "%4A":"J", "%4B":"K", "%4C":"L", "%4D":"M", "%4E":"N", "%4F":"O", \
    "%50":"P", "%51":"Q", "%52":"R", "%53":"S", "%54":"T", "%55":"U", "%56":"V", \
    "%57":"W", "%58":"X", "%59":"Y", "%5A":"Z", "%5B":"[", "%5C":"\\", "%5D":"]", \
    "%5E":"^", "%5F":"_", "%60":"`", "%61":"a", "%62":"b", "%63":"c", "%64":"d", \
    "%65":"e", "%66":"f", "%67":"g", "%68":"h", "%69":"i", "%6A":"j", \
    "%6B":"k", "%6C":"l", "%6D":"m", "%6E":"n", "%6F":"o", "%70":"p", \
    "%71":"q", "%72":"r", "%73":"s", "%74":"t", "%75":"u", "%76":"v", \
    "%77":"w", "%78":"x", "%79":"y", "%7A":"z", "%7B":"{", "%7C":"|", \
    "%7D":"}", "%7E":"~", "%E2%82%AC":"`", "%81":"", "%E2%80%9A":"‚", \
    "%C6%92":"ƒ", "%E2%80%9E":"„", "%E2%80%A6":"…", "%E2%80%A0":"†", \
    "%E2%80%A1":"‡", "%CB%86":"ˆ", "%E2%80%B0":"‰", "%C5%A0":"Š", \
    "%E2%80%B9":"‹", "%C5%92":"Œ", "%C5%8D":"", "%C5%BD":"Ž", \
    "%8F":"", "%C2%90":"", "%E2%80%98":"‘", "%E2%80%99":"’", \
    "%E2%80%9C":"“", "%E2%80%9D":"”", "%E2%80%A2":"•", "%E2%80%93":"–", \
    "%E2%80%94":"—", "%CB%9C":"˜", "%E2%84":"™", "%C5%A1":"š", "%E2%80":"›", \
    "%C5%93":"œ", "%9D":"", "%C5%BE":"ž", "%C5%B8":"Ÿ", "%C2%A1":"¡", \
    "%C2%A2":"¢", "%C2%A3":"£", "%C2%A4":"¤", "%C2%A5":"¥", "%C2%A6":"¦", \
    "%C2%A7":"§", "%C2%A8":"¨", "%C2%A9":"©", "%C2%AA":"ª", "%C2%AB":"«", \
    "%C2%AC":"¬", "%C2%AE":"®", "%C2%AF":"¯", "%C2%B0":"°", "%C2%B1":"±", \
    "%C2%B2":"²", "%C2%B3":"³", "%C2%B4":"´", "%C2%B5":"µ", "%C2%B6":"¶", \
    "%C2%B7":"·", "%C2%B8":"¸", "%C2%B9":"¹", "%C2%BA":"º", "%C2%BB":"»", \
    "%C2%BC":"¼", "%C2%BD":"½", "%C2%BE":"¾", "%C2%BF":"¿", "%C3%80":"À", \
    "%C3%81":"Á", "%C3%82":"Â", "%C3%83":"Ã", "%C3%84":"Ä", "%C3%85":"Å", \
    "%C3%86":"Æ", "%C3%87":"Ç", "%C3%88":"È", "%C3%89":"É", "%C3%8A":"Ê", \
    "%C3%8B":"Ë", "%C3%8C":"Ì", "%C3%8D":"Í", "%C3%8E":"Î", "%C3%8F":"Ï", \
    "%C3%90":"Ð", "%C3%91":"Ñ", "%C3%92":"Ò", "%C3%93":"Ó", "%C3%94":"Ô", \
    "%C3%95":"Õ", "%C3%96":"Ö", "%C3%97":"×", "%C3%98":"Ø", "%C3%99":"Ù", \
    "%C3%9A":"Ú", "%C3%9B":"Û", "%C3%9C":"Ü", "%C3%9D":"Ý", "%C3%9E":"Þ", \
    "%C3%9F":"ß", "%C3%A0":"à", "%C3%A1":"á", "%C3%A2":"â", "%C3%A3":"ã", \
    "%C3%A4":"ä", "%C3%A5":"å", "%C3%A6":"æ", "%C3%A7":"ç", "%C3%A8":"è", \
    "%C3%A9":"é", "%C3%AA":"ê", "%C3%AB":"ë", "%C3%AC":"ì", "%C3%AD":"í", \
    "%C3%AE":"î", "%C3%AF":"ï", "%C3%B0":"ð", "%C3%B1":"ñ", "%C3%B2":"ò", \
    "%C3%B3":"ó", "%C3%B4":"ô", "%C3%B5":"õ", "%C3%B6":"ö", "%C3%B7":"÷", \
    "%C3%B8":"ø", "%C3%B9":"ù", "%C3%BA":"ú", "%C3%BB":"û", "%C3%BC":"ü", \
    "%C3%BD":"ý", "%C3%BE":"þ", "%C3%BF":"ÿ"}

    encodings = []
    cc = 0 # character count
    cp = 0 # checkpoint
    code = list(code)

    # Finds all percent encodings in code
    while cc < len(code):
        if code[cc] == "%":
            cp = cc
            cc+=3
            if cc < len(code):
                while code[cc] == "%":
                    cc+=3
                    if cc >= len(code):
                        break
            try:
                key = "".join(code[cp:cc])
                if key in library:
                    for i in library[key]:
                        code[cp] = i
                        cp+=1
                    while cp != cc:
                        code[cp] = ""
                        cp+=1
                else:
                    keys = [key[i:i+3] for i in range(0, len(key), 3)]
                    for key in keys:
                        for i in library[key]:
                            code[cp] = i
                            code[cp+1] = ""
                            code[cp+2] = ""
                            cp+=3
                            
            except:
                continue
                    
        else:
            cc+=1
    code = "".join(code)
    return code


'''
CITATIONS
https://en.wikipedia.org/wiki/URL
https://www.w3schools.com/tags/ref_urlencode.asp
'''
