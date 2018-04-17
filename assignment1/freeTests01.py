#!/usr/bin/env python3

import assignment01

import unittest
from urllib.parse import urlsplit, parse_qs, unquote

class AssignmentOneFreeTestCase(unittest.TestCase):
    # FROM https://stackoverflow.com/questions/28500267/python-unittest-count-tests
    # Retrieved on 2018-01-20
    currentResult = None # holds last result object passed to run method

    @classmethod
    def setResult(cls, amount, errors, failures, skipped):
        cls.amount, cls.errors, cls.failures, cls.skipped = \
            amount, errors, failures, skipped

    def tearDown(self):
        amount = self.currentResult.testsRun
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        skipped = self.currentResult.skipped
        self.setResult(amount, errors, failures, skipped)

    @classmethod
    def tearDownClass(cls):
        print("\ntests run: " + str(cls.amount))
        print("errors: " + str(len(cls.errors)))
        print("failures: " + str(len(cls.failures)))
        success = cls.amount - len(cls.errors) - len(cls.failures)
        print("success: " + str(success))
        print("skipped: " + str(len(cls.skipped)))
        print("percent: " + "{0:.0f}%".format((success/cls.amount)*100))

    def run(self, result=None):
        self.currentResult = result # remember result for use in tearDown
        unittest.TestCase.run(self, result) # call superclass run method

    def test_only_scheme(self):
        self.assertEqual(assignment01.parse_url("about:"), 
            ('about', None, None, None, None, None))
        
    def parse_using_urllib(self, u):
        parsed = urlsplit(u)
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
    
    def test_example_from_assignment(self):
        u = 'http://localhost:8080/cats/cute/index.html?tag=fuzzy&tag=little+pawsies&show=data%26statistics#Statistics'
        self.assertEqual(assignment01.parse_url(u), 
            self.parse_using_urllib(u))

    def test_example_lots_of_percent(self):
        u = 'http://localhost:8080/cats%26scute/index%26shtml?tag=fuzzy&tag=little+pawsies&show=data%26statistics#Statistics%26s'
        self.assertEqual(assignment01.parse_url(u), 
            self.parse_using_urllib(u))

    def test_example_google(self):
        u = 'https://www.google.ca/search?q=%22cute+cats%22&ie=utf-8&oe=utf-8&gws_rd=cr&dcr=0&ei=_9hjWqm3FpWCjwP3pbjABA'
        self.assertEqual(assignment01.parse_url(u), 
            self.parse_using_urllib(u))

    def test_example_basic(self):
        u = 'https://www.google.ca/'
        self.assertEqual(assignment01.parse_url(u), 
            self.parse_using_urllib(u))
    
    def test_example_wikipedia(self):
        u = 'https://en.wikipedia.org/w/index.php?title=John_C._Fr%C3%A9mont&oldid=821454813#Early_life,_education,_and_career'
        self.assertEqual(assignment01.parse_url(u), 
            self.parse_using_urllib(u))
    
    def test_example_amazon(self):
        u = 'https://www.amazon.ca/Pusheen-Cat-2018-Wall-Calendar/dp/1449484700/ref=sr_1_1?ie=UTF8&qid=1516493370&sr=8-1&keywords=cute+cat+calendar'
        self.assertEqual(assignment01.parse_url(u), 
            self.parse_using_urllib(u))

    def test_example_maps(self):
        u = 'https://www.google.ca/maps/place/West+Edmonton+Mall/@53.5225155,-113.6416984,14z/data=!4m5!3m4!1s0x53a020573a8614db:0x8546a29e09b26fcb!8m2!3d53.5225155!4d-113.6241889'
        self.assertEqual(assignment01.parse_url(u), 
            self.parse_using_urllib(u))

    def test_example_youtube(self):
        u = 'https://youtu.be/F22Bop-_sxo?t=13s'
        self.assertEqual(assignment01.parse_url(u), 
            self.parse_using_urllib(u))
        
    def test_example_sso(self):
        u = 'https://login.ualberta.ca/module.php/core/loginuserpass.php?AuthState=_d206496583a0ee5507aded2ee743bce74e885a5610%3Ahttps%3A%2F%2Flogin.ualberta.ca%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Dhttps%253A%252F%252Feclass.srv.ualberta.ca%252Fsp%26cookieTime%3D1516493628%26RelayState%3Dhttps%253A%252F%252Feclass.srv.ualberta.ca%252Fauth%252Fsaml%252Findex.php%253Fwantsurl%253Dhttps%25253A%25252F%25252Feclass.srv.ualberta.ca%25252F'
        self.assertEqual(assignment01.parse_url(u), 
            self.parse_using_urllib(u))

    def test_example_youtube(self):
        u = 'https://docs.google.com/document/d/1HLAtmHw0OWmrthyO9MDZI7wcs13WxC92H_PNpwrGF2w/edit#heading=h.n76a9i6p9x2f'
        self.assertEqual(assignment01.parse_url(u), 
            self.parse_using_urllib(u))

if __name__ == '__main__':
    unittest.main()
