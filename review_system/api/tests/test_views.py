from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from api.models import Company, Review
import json


class TestViews(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        u = User.objects.create_user('MaddieKan', 'dr.almanovamadina@gmail.com', 'MaddieKan')
        a = User.objects.create_user('admin', 'admin@gmail.com', 'admin')
        a.is_staff = 1
        a.save()
        c = Company.objects.create(name='1Fit', description='Gym subscriptions',
                               address='Kazakhstan, Almaty, Makataev st. 117')
        Review.objects.create(rating=4, title='First Review', summary='Summary', ip=2130706433, company=c, reviewer=u)
        self.login('MaddieKan', 'MaddieKan')

    def login(self, login, password):
        response = self.api_client.post(reverse('login'), {"username": login, "password": password})
        response_content = json.loads(response.content.decode('utf-8'))
        self.token = response_content["token"]
        self.api_client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)

    def get_request(self, url):
        response = self.api_client.get(url, format='json')
        response_content = json.loads(response.content.decode('utf-8'))
        return response, response_content

    def post_request(self, url, data):
        response = self.api_client.post(url, data, format='json')
        response_content = json.loads(response.content.decode('utf-8'))
        return response, response_content

    def put_request(self, url, data):
        response = self.api_client.put(url, data, format='json')
        response_content = json.loads(response.content.decode('utf-8'))
        return response, response_content

    def delete_request(self, url):
        response = self.api_client.delete(url, format='json')
        response_content = json.loads(response.content.decode('utf-8'))
        return response, response_content

    def test_sign_up_POST(self):
        url = reverse('sign_up')
        data = {"username": "test", "email": "test@gmail.com", "password": "test", "first_name": "test",
                "last_name": "test", "is_staff": 0}
        response = self.api_client.post(url, data, format='json')
        self.assertEquals(response.status_code, 201)

    def test_companies_list_GET(self):
        response, response_content = self.get_request(reverse('companies'))
        data = [{'id': 1, 'name': '1Fit', 'description': 'Gym subscriptions',
                 'address': 'Kazakhstan, Almaty, Makataev st. 117'}]
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_content, data)

    def test_companies_list_POST(self):
        data = {"name": "Codebusters", "description": "desc", "address": "Kazakhstan, Almaty, Makataev st. 117"}
        response, response_content = self.post_request(reverse('companies'), data)
        res_data = {"id": 2, "name": "Codebusters", "description": "desc",
                    "address": "Kazakhstan, Almaty, Makataev st. 117"}
        self.assertEquals(response.status_code, 201)
        self.assertEquals(res_data, response_content)

    def test_company_details_GET(self):
        response, response_content = self.get_request(reverse('company_details', args=[1]))
        data = {'id': 1, 'name': '1Fit', 'description': 'Gym subscriptions',
                 'address': 'Kazakhstan, Almaty, Makataev st. 117'}
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_content, data)

    def test_company_details_PUT(self):
        data = {"name": "1fit", "description": "desc", "address": "Kazakhstan, Almaty, Makataev st. 117"}
        response, response_content = self.put_request(reverse('company_details', args=[1]), data)
        res_data = {"id": 1, "name": "1fit", "description": "desc", "address": "Kazakhstan, Almaty, Makataev st. 117"}
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_content, res_data)

    def test_company_details_DELETE(self):
        response, response_content = self.delete_request(reverse('company_details', args=[1]))
        data = {'deleted': True}
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_content, data)

    def test_reviews_list_not_admin_GET(self):
        response, response_content = self.get_request(reverse('reviews_full_list'))
        data = {'details': 'permission denied'}
        self.assertEquals(response.status_code, 403)
        self.assertEquals(response_content, data)

    def test_reviews_list_admin_GET(self):
        self.login('admin', 'admin')
        response, response_content = self.get_request(reverse('reviews_full_list'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_content[0]['title'], 'First Review')

    def test_reviews_list_POST(self):
        data = {"rating": 5, "title": "Second Review", "summary": "Summary", "ip": "192.168.0.1", "company": 1,
                "reviewer": 1}
        response, response_content = self.post_request(reverse('reviews_full_list'), data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response_content['title'], 'Second Review')

    def test_review_details_GET(self):
        response, response_content = self.get_request(reverse('review_details', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_content['title'], 'First Review')

    def test_review_details_PUT(self):
        data = {"rating": 5, "title": "Edited First Review", "summary": "Summary", "company": 1}
        response, response_content = self.put_request(reverse('review_details', args=[1]), data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_content['title'], 'Edited First Review')

    def test_review_details_DELETE(self):
        response, response_content = self.delete_request(reverse('review_details', args=[1]))
        data = {'deleted': True}
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_content, data)

    def test_user_reviews_GET(self):
        response, response_content = self.get_request(reverse('user_reviews'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_content[0]['title'], 'First Review')




