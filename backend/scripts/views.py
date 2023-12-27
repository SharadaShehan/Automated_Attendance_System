from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, exceptions
from database.models import CustomUser, Company, Role
import csv, json

class InitView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Hello World'})



# class MiddlewareUpdateUserAttendanceEnterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = []
#
#     def update(self, instance, validated_data):
#         try:
#             user_api_code = self.context['request'].data.get('user_api_code', None)
#             obj_from_db = CustomUser.objects.get(user_api_code=user_api_code)
#         except Exception as ex:
#             raise serializers.ValidationError("Invalid user data")
#
#         if obj_from_db.id == instance.id :
#             try:
#                 date = self.context['request'].data.get('date', None)
#                 time = self.context['request'].data.get('time', None)
#                 date_strings_list = date.split('-')
#                 time_strings_list = time.split('-')
#                 if len(date_strings_list) != 3 or len(time_strings_list) != 2:
#                     raise Exception()
#                 date_int_list = [int(i) for i in date_strings_list]
#                 time_int_list = [int(i) for i in time_strings_list]
#
#                 attendance_obj = json.loads(instance.attendance)
#
#                 if date_strings_list[0] in attendance_obj:
#                     if date_strings_list[1] in attendance_obj[date_strings_list[0]]:
#                         if date_strings_list[2] in attendance_obj[date_strings_list[0]][date_strings_list[1]]:
#                             pass
#                         else:
#                             attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]] = {'entrance': [], 'leave': []}
#                     else:
#                         attendance_obj[date_strings_list[0]][date_strings_list[1]] = { date_strings_list[2]: {'entrance': [], 'leave': []}}
#                 else:
#                     attendance_obj[date_strings_list[0]] = { date_strings_list[1]: {date_strings_list[2]: {'entrance': [], 'leave': []}}}
#
#                 attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['entrance'].append(time)
#
#                 instance.attendance = json.dumps(attendance_obj)
#                 instance.save()
#
#             except:
#                 raise exceptions.NotAcceptable('Invalid Date/Time format !')
#         else:
#             raise serializers.ValidationError("Invalid user details")
#
#         return instance
#
# class MiddlewareUpdateUserAttendanceLeaveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = []
#
#     def update(self, instance, validated_data):
#         try:
#             user_api_code = self.context['request'].data.get('user_api_code', None)
#             obj_from_db = CustomUser.objects.get(user_api_code=user_api_code)
#         except Exception as ex:
#             raise serializers.ValidationError("Invalid user data")
#
#         if obj_from_db.id == instance.id:
#             try:
#                 date = self.context['request'].data.get('date', None)
#                 time = self.context['request'].data.get('time', None)
#                 date_strings_list = date.split('-')
#                 time_strings_list = time.split('-')
#                 if len(date_strings_list) != 3 or len(time_strings_list) != 2:
#                     raise Exception()
#                 date_int_list = [int(i) for i in date_strings_list]
#                 time_int_list = [int(i) for i in time_strings_list]
#
#                 attendance_obj = json.loads(instance.attendance)
#
#                 if date_strings_list[0] in attendance_obj:
#                     if date_strings_list[1] in attendance_obj[date_strings_list[0]]:
#                         if date_strings_list[2] in attendance_obj[date_strings_list[0]][date_strings_list[1]]:
#                             pass
#                         else:
#                             attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]] = {'entrance': [], 'leave': []}
#                     else:
#                         attendance_obj[date_strings_list[0]][date_strings_list[1]] = { date_strings_list[2]: {'entrance': [], 'leave': []}}
#                 else:
#                     attendance_obj[date_strings_list[0]] = { date_strings_list[1]: {date_strings_list[2]: {'entrance': [], 'leave': []}}}
#
#                 attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['leave'].append(time)
#
#                 instance.attendance = json.dumps(attendance_obj)
#                 instance.save()
#
#             except:
#                 raise exceptions.NotAcceptable('Invalid Date/Time format !')
#         else:
#             raise serializers.ValidationError("Invalid user details")
#
#         return instance
