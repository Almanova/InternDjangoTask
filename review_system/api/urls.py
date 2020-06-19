from django.urls import path
import api.views as views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('sign_up/', views.sign_up),
    path('companies/', views.companies_list, name='companies'),
    path('companies/<int:company_id>/', views.company_details),
    path('reviews/', views.reviews_full_list, name='reviews_full_list'),
    path('login/', obtain_jwt_token, name='login'),
    path('my_reviews/', views.user_reviews, name='user_reviews'),
    path('reviews/<int:review_id>/', views.review_details)
]