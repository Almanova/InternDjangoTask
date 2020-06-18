from django.urls import path
import api.views as views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('sign_up/', views.sign_up),
    path('companies/', views.companies_list, name='companies'),
    path('companies/<int:company_id>/', views.company_details)
]