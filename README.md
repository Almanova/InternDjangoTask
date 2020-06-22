# Review System

Api for a review system. New users can register, already existing - add reviews for companies that are in the database. Users can retrieve their reviews, also update and delete them. Administrators can retrieve a full list of all reviews from database.

Main django-application 'api' contains all the models, serializers, urls, views and tests for them.

InternDjangoTask/  
├── env/  
├── review_system/  
│   ├── api/  
│   └── review_system/

## Installation

Installing following modules for virtualenv:
```bash
pip freeze
asgiref==3.2.9
coverage==5.1
Django==3.0.7
django-ipware==2.1.0
djangorestframework==3.11.0
djangorestframework-jwt==1.11.0
PyJWT==1.7.1
pytz==2020.1
sqlparse==0.3.1
```

Running with 
```bash
python manage.py runserver
```
within review_system directory

## Primary Data

Adding one admin-user and regular user is enough for testing api. All the other data can be added while testing the api.

```bash
u = User.objects.create_user('MaddieKan', 'dr.almanovamadina@gmail.com', 'MaddieKan')
a = User.objects.create_user('admin', 'admin@gmail.com', 'admin')
a.is_staff = 1
a.save()
```

## Api documentation (Postman collection)

[Apidoc](https://documenter.getpostman.com/view/10904618/SzzoabTV)
