from django.test import TestCase

from users.models import CustomUser


class PuppyTest(TestCase):
    """ Test module for Puppy model """
    def setUp(self):
        CustomUser.objects.create(
            email='Casper@gmail.com', password="12345", balance=500)
        CustomUser.objects.create(
            email='Casper1@gmail.com', password="12345", balance=300)
        
        
    def test_puppy_breed(self):
        puppy_casper = CustomUser.objects.get(email='Casper@gmail.com')
        puppy_muffin = CustomUser.objects.get(email='Casper1@gmail.com')
        self.assertEqual(
            puppy_casper.get_user_base_data(), "Casper@gmail.com 500")
        self.assertEqual(
            puppy_muffin.get_user_base_data(), "Casper1@gmail.com 300")