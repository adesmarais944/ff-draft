import os
import django
from django.test import RequestFactory

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Import the players function
from main.api import players

# Create a mock request
factory = RequestFactory()
request = factory.get('/fake-path')

# Call the players function
players(request)

print("Players fetched and created successfully.")