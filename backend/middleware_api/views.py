from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from database.models import CustomUser, Company
from .serializers import MiddlewareCreateUserSerializer, MiddlewareCreateCompanySerializer
# from .ml_model import MLModel
from werkzeug.security import check_password_hash
import secrets


class MiddlewareCreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = MiddlewareCreateUserSerializer


class MiddlewareCreateCompanyView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = MiddlewareCreateCompanySerializer

    def create(self, request, *args, **kwargs):
        # Call the parent class's create method to perform the actual object creation
        response = super().create(request, *args, **kwargs)

        init_token = self.generate_init_token(64)
        company = Company.objects.get(name=request.data.get('name'))
        company.init_token = init_token
        company.save()

        # Customize the response data as needed
        custom_data = {
            'message': 'Company created successfully',
            'data': response.data,
            'init_token': init_token
        }
        # Replace the original data with the custom data
        response.data = custom_data
        # Optionally, you can also customize the status code
        response.status_code = status.HTTP_201_CREATED
        return response

    @staticmethod
    def generate_init_token(length):
        # Generate a random string with the specified length
        random_string = secrets.token_hex(length // 2)
        return random_string[:length]


class CompanyPortalLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password').strip()
        init_token = request.headers.get('Authorization', None)
        try:
            company = Company.objects.get(username=username)
            if check_password_hash(company.password, password) and company.init_token == init_token:
                access_token = self.generate_access_token(64)
                company.access_token = access_token
                company.save()
                return Response({'message': 'Login successful!', 'access_token': access_token})
            else:
                return Response({'message': 'Incorrect Credentials'}, status=400)
        except Company.DoesNotExist:
            return Response({'message': 'Invalid Login'}, status=400)

    @staticmethod
    def generate_access_token(length):
        # Generate a random string with the specified length
        random_string = secrets.token_hex(length // 2)
        return random_string[:length]


# class MLModelInputView(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             company = Company.objects.get_company()
#             if company.access_token == request.headers.get('Authorization', None):
#                 if MLModel.add_task(request.data):
#                     return Response({'message': 'Input added to queue'})
#                 return Response({'message': 'Failed to add input to queue'}, status=400)
#             else:
#                 return Response({'message': 'Invalid access token'}, status=401)
#         except Company.DoesNotExist:
#             return Response({'message': 'Company does not exist'}, status=400)
