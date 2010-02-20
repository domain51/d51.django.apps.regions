from django import test

class TestCase(test.TestCase):
    pass

class Client(test.client.Client):
    pass

