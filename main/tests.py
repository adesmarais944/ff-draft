from django.test import TestCase
from django.urls import reverse

class BasicViewTests(TestCase):
    def test_home_page_redirects(self):
        """
        Test that the home page redirects (returns 302 status code).
        This is expected if the view requires login.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
    
    def test_drafts_page_status_code(self):
        """
        Test that the drafts page exists.
        If this page requires login, update this test to expect 302 instead of 200.
        """
        response = self.client.get('/drafts/')
        self.assertEqual(response.status_code, 200)