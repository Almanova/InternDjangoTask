from django.shortcuts import render
from rest_framework.response import Response
from api.serializers import UserSerializer, CompanySerializer, ReviewSerializer
from rest_framework import status
from api.models import Company, Review
from rest_framework.views import APIView
import ipaddress
from ipware import get_client_ip


class ReviewRelated:
    def convert_ip(self, str_ip):
        int_ip = int(ipaddress.IPv4Address(str_ip))
        return int_ip

    def get_object(self, review_id):
        try:
            return Review.objects.get(id=review_id)
        except Review.DoesNotExist as e:
            return Response({'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewsFullListAPIView(APIView, ReviewRelated):
    def get(self, request):
        if request.user.is_staff == 1:
            reviews = Review.objects.all()
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response({'details': 'permission denied'},
                        status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        request.data["reviewer"] = request.user.id
        ip = get_client_ip(request)[0]
        request.data["ip"] = self.convert_ip(ip)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReviewDetailsAPIView(APIView, ReviewRelated):
    def get(self, request, review_id):
        review = self.get_object(review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    def put(self, request, review_id):
        review = self.get_object(review_id)
        request.data["reviewer"] = request.user.id
        ip = get_client_ip(request)[0]
        request.data["ip"] = self.convert_ip(ip)
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response({'error': serializer.errors},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, review_id):
        review = self.get_object(review_id)
        review.delete()
        return Response({'deleted': True},
                        status=status.HTTP_200_OK)



