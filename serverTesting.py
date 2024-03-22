import http
import unittest
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler
import http.client
import json
import threading

#Testing for GET Method
class TestServerGET(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8000)
        cls.server = HTTPServer(cls.server_address, SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()
    

    def test_get_method(self):
        # Connect to the server and send a GET request
        connection = http.client.HTTPConnection(*self.server_address)
        connection.request('GET', '/')
        respone = connection.getresponse()

        # Read and Decode the response
        data = respone.read().decode()
        connection.close()

        #check That the resopnse as expected
        self.assertEqual(respone.status, 200)
        self.assertEqual(respone.reason, 'OK')
        self.assertEqual(respone.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        respone_data = json.loads(data)
        self.assertEqual(respone_data, {'message': 'This is a GET request response'})

#Testing for POST Method
class TestServerPOST(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8000)
        cls.server = HTTPServer(cls.server_address, SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    def test_post_method(self):
        # Connect to the server and send a POST request
        connection = http.client.HTTPConnection(*self.server_address)
        headers = {'Content-type': 'application/json'} #pass headers
        body = json.dumps({'username': 'test_user'}) #pass values in body (key => value)
        connection.request('POST', '/', body, headers) #get connection request
        response = connection.getresponse()

        # Read and decode the response
        data = response.read().decode()
        connection.close()

        # Check that the response is as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data, {'received': {'username': 'test_user'}})

if __name__ == '__main__':
    unittest.main()