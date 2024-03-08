from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from database.models import CustomUser, Company
from .serializers import MiddlewareCreateUserSerializer, MiddlewareCreateCompanySerializer
# from .ml_model import MLModel
from django.conf import settings
from werkzeug.security import check_password_hash
import secrets
import json
import hashlib
import re
import datetime

hub_secret_key = settings.HUB_SECRET_KEY
hashed_hub_secret_key = hashlib.sha256(hub_secret_key.encode('utf-8')).hexdigest()
min_minutes_threshold = int(settings.MIN_MINUTES_THRESHOLD)

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


class UpdateUserEntranceView(APIView):
    def get(self, request, *args, **kwargs):
        secret_key = request.headers.get('hub-secret-key', None)
        if secret_key == hashed_hub_secret_key:
            user_id = kwargs.get('id')
            time_received = f"{str(kwargs.get('hour')).zfill(2)}-{str(kwargs.get('minute')).zfill(2)}"
            # time must be received in the format: '%H-%M'
            if user_id and time_received:
                try:
                    # check if datetime is in the correct format
                    if not re.match(r'^\d{2}-\d{2}$', time_received):
                        return Response({'message': 'Invalid time format'}, status=400)
                    date = datetime.datetime.now().strftime("%Y-%m-%d")
                    date_strings_list = date.split("-")

                    detected_user = CustomUser.objects.get(id=user_id)
                    attendance_obj = json.loads(detected_user.attendance)

                    # Check if the date is already in the attendance object unlless create it
                    if date_strings_list[0] in attendance_obj:
                        if date_strings_list[1] in attendance_obj[date_strings_list[0]]:
                            if date_strings_list[2] in attendance_obj[date_strings_list[0]][date_strings_list[1]]:
                                pass
                            else:
                                attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]] = {
                                    'entrance': [], 'leave': []}
                        else:
                            attendance_obj[date_strings_list[0]][date_strings_list[1]] = {
                                date_strings_list[2]: {'entrance': [], 'leave': []}}
                    else:
                        attendance_obj[date_strings_list[0]] = {
                            date_strings_list[1]: {date_strings_list[2]: {'entrance': [], 'leave': []}}}

                    time_format = '%H-%M'  # expected format of time
                    entrance_list_of_day = attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['entrance']
                    if len(entrance_list_of_day) > 0:
                        last_entrance = datetime.datetime.strptime(entrance_list_of_day[-1], time_format)
                        current_entrance = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H-%M").split()[1], time_format)
                        # Check if the time difference between the last entrance and the current entrance is
                        # less than the minimum minutes threshold
                        received_time = datetime.datetime.strptime(time_received, time_format)
                        if (current_entrance - last_entrance) < datetime.timedelta(minutes=min_minutes_threshold) or \
                                (last_entrance - received_time) < datetime.timedelta(minutes=min_minutes_threshold):
                            return Response({'message': 'Entrance not updated. Minimum minutes threshold not reached'}, status=400)
                    attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['entrance'].append(time_received)

                    # If updated successfully, save the user
                    detected_user.attendance = json.dumps(attendance_obj)
                    detected_user.save()

                    return Response({'message': 'Entrance updated successfully', 'firstName': detected_user.first_name,
                                     'lastName': detected_user.last_name, 'time': time_received})
                except CustomUser.DoesNotExist:
                    return Response({'message': 'User does not exist'}, status=400)
            else:
                return Response({'message': 'Invalid path parameters'}, status=400)
        else:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


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
