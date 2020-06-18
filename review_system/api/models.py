from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=200)


class Review(models.Model):
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=64)
    summary = models.TextField()
    ip = models.IntegerField()
    submission_date = models.DateTimeField(auto_now_add=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
