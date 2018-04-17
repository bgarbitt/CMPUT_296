# Weclome to Assignment #1!

# Your name:
# The date:
# The names of any students you consulted with:

# Paste the license you choose for your assignment here.

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
    scheme_ends = url.index(":")
    scheme = url[0:scheme_ends]
    return (
        scheme,
        None,
        None,
        None,
        None,
        None
    )

