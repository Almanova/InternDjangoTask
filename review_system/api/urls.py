from django.urls import path
from api.views import views_company_fbv as fbv, views_review_cbv as cbv
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('sign_up/', fbv.sign_up, name='sign_up'),
    path('companies/', fbv.companies_list, name='companies'),
    path('companies/<int:company_id>/', fbv.company_details, name='company_details'),
    path('reviews/', cbv.ReviewsFullListAPIView.as_view(), name='reviews_full_list'),
    path('login/', obtain_jwt_token, name='login'),
    path('my_reviews/', fbv.user_reviews, name='user_reviews'),
    path('reviews/<int:review_id>/', cbv.ReviewDetailsAPIView.as_view(), name='review_details')
]