from django.test import TestCase


with open('../../secret_key.txt', 'rt') as secret:
    key = secret.read()

print(key)