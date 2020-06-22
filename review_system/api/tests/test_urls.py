from django.test import SimpleTestCase
from django.urls import reverse, resolve
from api.views import views_company_fbv as fbv, views_review_cbv as cbv
from rest_framework_jwt.views import obtain_jwt_token
import json


class TestUrls(SimpleTestCase):
    def test_sign_up(self):
        url = reverse('sign_up')
        self.assertEquals(resolve(url).func, fbv.sign_up)

    def test_companies(self):
        url = reverse('companies')
        self.assertEquals(resolve(url).func, fbv.companies_list)

    def test_company_details(self):
        url = reverse('company_details', args=[1])
        self.assertEquals(resolve(url).func, fbv.company_details)

    def test_reviews_full_list(self):
        url = reverse('reviews_full_list')
        self.assertEquals(resolve(url).func.__name__, cbv.ReviewsFullListAPIView.as_view().__name__)

    def test_login(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, obtain_jwt_token)

    def test_user_reviews(self):
        url = reverse('user_reviews')
        self.assertEquals(resolve(url).func, fbv.user_reviews)

    def test_review_details(self):
        url = reverse('review_details', args=[1])
        self.assertEquals(resolve(url).func.__name__, cbv.ReviewDetailsAPIView.as_view().__name__)