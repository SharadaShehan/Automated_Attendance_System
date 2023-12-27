from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, exceptions
from database.models import CustomUser, Company, Role
import csv, json


class InitView(APIView):
    def get(self, request, *args, **kwargs):

        try:
            # delete all data
            CustomUser.objects.all().delete()
            Role.objects.all().delete()
            Company.objects.all().delete()

            with open('scripts/data/Roles.csv', 'r') as f:
                reader = csv.reader(f)
                csv_header = next(reader)

                # create default role
                default_role_data = next(reader)
                name, is_manager, is_executive = default_role_data[0].strip(), int(default_role_data[1].strip()), int(default_role_data[2].strip())

                default_role = Role.objects.create(name=name, is_manager=is_manager, is_executive=is_executive)
                default_role.save()

                # create other roles
                for row in reader:
                    name, is_manager, is_executive = row[0].strip(), int(row[1].strip()), int(row[2].strip())
                    role = Role.objects.create(name=name, is_manager=is_manager, is_executive=is_executive)
                    role.save()

            company = Company.objects.create(name='Apple', default_role=default_role)
            company.save()

            # create users
            with open('scripts/data/Employees.csv', 'r') as f:
                reader = csv.reader(f)
                csv_header = next(reader)

                for row in reader:
                    email, password, role, first_name, last_name, gender = row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip(), row[5].strip()
                    role_obj = Role.objects.get(name=role)
                    employee = CustomUser.objects.create(email=email, role=role_obj, first_name=first_name, last_name=last_name,
                                                         gender=gender, encodings=json.dumps([]), picture=None, attendance='{}')
                    employee.set_password(password)
                    employee.save()


            with open('scripts/data/Attendance.csv', 'r') as f:
                reader = csv.reader(f)
                csv_header = next(reader)

                # create default role
                for row in reader:
                    email, datetime, entrance = row[0].strip(), row[1].strip(), bool(int(row[2].strip()))
                    user = CustomUser.objects.get(email=email)
                    attendance_obj = json.loads(user.attendance)
                    date, time = datetime.split(' ')
                    date_strings_list = date.split('-')
                    time_strings_list = time.split('-')
                    if len(date_strings_list) != 3 or len(time_strings_list) != 2:
                        raise Exception("Invalid date or time format")

                    if date_strings_list[0] in attendance_obj:
                        if date_strings_list[1] in attendance_obj[date_strings_list[0]]:
                            if date_strings_list[2] in attendance_obj[date_strings_list[0]][date_strings_list[1]]:
                                pass
                            else:
                                attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]] = {'entrance': [], 'leave': []}
                        else:
                            attendance_obj[date_strings_list[0]][date_strings_list[1]] = { date_strings_list[2]: {'entrance': [], 'leave': []}}
                    else:
                        attendance_obj[date_strings_list[0]] = { date_strings_list[1]: {date_strings_list[2]: {'entrance': [], 'leave': []}}}

                    if entrance:
                        attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['entrance'].append(time)
                    else:
                        attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['leave'].append(time)

                    user.attendance = json.dumps(attendance_obj)
                    user.save()

            print("Srcripts executed successfully")
            return Response({'message': 'Hello World'})

        except Exception as ex:
            print(ex)
            return Response({'message': f"Error: {ex}"}, status=400)

