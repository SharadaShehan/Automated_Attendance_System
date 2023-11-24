from rest_framework import generics
from database.models import CustomUser, Company
from .serializers import MiddlewareCreateUserSerializer, MiddlewareCreateCompanySerializer, MiddlewareUpdateUserAttendanceEnterSerializer, MiddlewareUpdateUserAttendanceLeaveSerializer


class MiddlewareCreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = MiddlewareCreateUserSerializer

class MiddlewareCreateCompanyView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = MiddlewareCreateCompanySerializer

class MiddlewareUpdateUserAttendanceEnterView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = MiddlewareUpdateUserAttendanceEnterSerializer

class MiddlewareUpdateUserAttendanceLeaveView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = MiddlewareUpdateUserAttendanceLeaveSerializer