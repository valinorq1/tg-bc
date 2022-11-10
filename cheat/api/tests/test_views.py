from datetime import datetime

from django.urls import reverse
from loguru import logger
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from api.views import ViewTaskViewSet
from users.models import CustomUser, ViewTask


class ViewTaskViewSetTestCase(APITestCase):
    
    def test_get_view_task(self):
        response = self.client.get(reverse('view_task-detail', kwargs={'pk': 1}))
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    """ def test_view_task_create(self):
        pass """
    
    
    def test_api_jwt(self):
        url = reverse("token_obtain_pair")
        u = CustomUser.objects.create_user(email='val1@gmail.com', password='en1996ru', balance=500000)
        u.save()
        response = self.client.post(url, {'email':'val1@gmail.com', 'password':'en1996ru'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        
        token = response.data['access']
        
        
        
""" class TestCaseBase(APITestCase):
    
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email='test@user.me', password='12345678'
        )
        return user
        
    
    @property
    def bearer_token(self):
        # assuming there is a user in User model
        refresh = RefreshToken.for_user(self.test_create_user)
        logger.debug(self.test_create_user())
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'} """
    
    


""" class CategoriesTestClass(TestCaseBase):
    #url = reverse('view_task-detail', kwargs={'pk': 1})
    
    def SetUp(self):
        self.factory = APIRequestFactory()
        self.user = self.user
        

    def test_get_view_task(self):
        logger.debug(self.user)
        task = ViewTask.objects.create(channel="123123", post_id=5, task_duration=500, count_per_post=50, count_avg=100, user_id=self.user)
        self.client.post(reverse('view_task-detail', kwargs={'pk': 1}))
    
    def test_get_views_task_no_auth(self):
        response = self.client.get(reverse('view_task-detail', kwargs={'pk': 1}))
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data
        )

    def test_get_list(self):
        response = self.client.get(reverse('view_task-detail', kwargs={'pk': 1}), **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK) """