from django.test import TestCase

# Create your tests here.


class TestStringMethods(TestCase):
    def test_length(self):
        self.assertEqual(len('yatube'), 6)
