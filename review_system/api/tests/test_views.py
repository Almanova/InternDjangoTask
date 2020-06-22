from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from api.models import Company, Review
import json


class TestFBVViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.api_client = APIClient()
        User.objects.create_user('MaddieKan', 'dr.almanovamadina@gmail.com', 'MaddieKan')
        Company.objects.create(name='1Fit', description='Gym subscriptions',
                               address='Kazakhstan, Almaty, Makataev st. 117')
        url = reverse('login')
        response = self.client.post(url, {"username": "MaddieKan", "password": "MaddieKan"})
        response_content = json.loads(response.content.decode('utf-8'))
        self.token = response_content["token"]

    def test_sign_up_POST(self):
        url = reverse('sign_up')
        data = {"username": "test", "email": "test@gmail.com", "password": "test", "first_name": "test",
                "last_name": "test", "is_staff": 0}
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, 201)

    def test_companies_list_GET(self):
        url = reverse('companies')
        response = self.client.get(url, HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEquals(response.status_code, 200)
        data = [{'id': 1, 'name': '1Fit', 'description': 'Gym subscriptions', 'address': 'Kazakhstan, Almaty, Makataev st. 117'}]
        self.assertEquals(response_content, data)

    # def test_user_reviews(self):
    #     url = reverse('login')
    #     response = self.client.post(url, {"username": "admin", "password": "admin"})
    #     response_content = json.loads(response.content.decode('utf-8'))
    #     print(response_content)
    #     token = response_content["token"]
    #     print(token)
    #
    #     url = reverse('user_reviews')
    #     response = self.client.get(url, HTTP_AUTHORIZATION='JWT {}'.format(token))
    #     response_content = json.loads(response.content.decode('utf-8'))
    #     print(response_content)
    #     self.assertEquals(response.status_code, 200)
    #
    # def test_adding_review(self):
    #     url = reverse('login')
    #     response = self.client.post(url, {"username": "admin", "password": "admin"})
    #     response_content = json.loads(response.content.decode('utf-8'))
    #     token = response_content["token"]
    #
        # url = reverse('reviews_full_list')
        # data = {"rating": 5, "title": "Second Review", "summary": "Summary", "ip": "192.168.0.1", "company": 1, "reviewer": 1}
        # c = APIClient()
        # c.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        # response = c.post(url, data, format='json')
        # response_content = json.loads(response.content.decode('utf-8'))
        # print(response_content)
        # self.assertEquals(response.status_code, 201)
