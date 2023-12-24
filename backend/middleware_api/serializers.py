from database.models import CustomUser, Role, Company
from rest_framework import serializers, exceptions
import json
import face_recognition
import numpy as np
from werkzeug.security import generate_password_hash

class MiddlewareCreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'gender']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        user.role = Company.objects.get_company().default_role
        user.attendance = '{}'

        if password:
            user.set_password(password)
            user.save()
        else:
            user.delete()
            raise exceptions.ValidationError({'password': 'Password is required'})

        try:
            converted_photo = np.array(self.context['request'].data.get('photo')).astype(np.uint8)
            encodings = face_recognition.face_encodings(converted_photo)[0]
            json_encodings = json.dumps(encodings.tolist())
            user.encodings = json_encodings
        except:
            user.delete()
            raise exceptions.ValidationError({'photo': 'Invalid photo'})

        return user


class MiddlewareCreateCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['name', 'username', 'password']

    def create(self, validated_data):
        default_executive_role = Role.objects.create(name='Executive', is_manager=True, is_executive=True)
        default_employee_role = Role.objects.create(name='Employee', is_manager=False, is_executive=False)
        default_executive_account = self.context['request'].data.get('default_executive_account')
        try:
            converted_photo = np.array(default_executive_account['photo']).astype(np.uint8)
            encodings = face_recognition.face_encodings(converted_photo)[0]
            json_encodings = json.dumps(encodings.tolist())
            default_executive = CustomUser.objects.create(email=default_executive_account['email'],
                                                          role=default_executive_role,
                                                          first_name=default_executive_account['first_name'],
                                                          last_name=default_executive_account['last_name'],
                                                          gender=default_executive_account['gender'],
                                                          encodings=json_encodings,
                                                          picture=None,
                                                          attendance='{}')
            default_executive.set_password(default_executive_account['password'])
            default_executive.save()
            company_password_hashed = generate_password_hash(validated_data.get('password').strip(), method='scrypt')
            company = Company.objects.create(name=validated_data.get('name'),
                                            username=validated_data.get('username'),
                                            password=company_password_hashed,
                                            default_role=default_employee_role)
            company.save()
        except Exception as ex:
            if default_executive_role:
                default_executive_role.delete()
            if default_employee_role:
                default_employee_role.delete()
            try:
                if default_executive:
                    default_executive.delete()
            except:
                pass
            raise serializers.ValidationError(f"Error in creating company: {ex}")
        return company


class MiddlewareUpdateUserAttendanceEnterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = []

    def update(self, instance, validated_data):
        try:
            user_api_code = self.context['request'].data.get('user_api_code', None)
            obj_from_db = CustomUser.objects.get(user_api_code=user_api_code)
        except Exception as ex:
            raise serializers.ValidationError("Invalid user data")

        if obj_from_db.id == instance.id :
            try:
                date = self.context['request'].data.get('date', None)
                time = self.context['request'].data.get('time', None)
                date_strings_list = date.split('-')
                time_strings_list = time.split('-')
                if len(date_strings_list) != 3 or len(time_strings_list) != 2:
                    raise Exception()
                date_int_list = [int(i) for i in date_strings_list]
                time_int_list = [int(i) for i in time_strings_list]

                attendance_obj = json.loads(instance.attendance)

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

                attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['entrance'].append(time)

                instance.attendance = json.dumps(attendance_obj)
                instance.save()

            except:
                raise exceptions.NotAcceptable('Invalid Date/Time format !')
        else:
            raise serializers.ValidationError("Invalid user details")

        return instance

class MiddlewareUpdateUserAttendanceLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = []

    def update(self, instance, validated_data):
        try:
            user_api_code = self.context['request'].data.get('user_api_code', None)
            obj_from_db = CustomUser.objects.get(user_api_code=user_api_code)
        except Exception as ex:
            raise serializers.ValidationError("Invalid user data")

        if obj_from_db.id == instance.id:
            try:
                date = self.context['request'].data.get('date', None)
                time = self.context['request'].data.get('time', None)
                date_strings_list = date.split('-')
                time_strings_list = time.split('-')
                if len(date_strings_list) != 3 or len(time_strings_list) != 2:
                    raise Exception()
                date_int_list = [int(i) for i in date_strings_list]
                time_int_list = [int(i) for i in time_strings_list]

                attendance_obj = json.loads(instance.attendance)

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

                attendance_obj[date_strings_list[0]][date_strings_list[1]][date_strings_list[2]]['leave'].append(time)

                instance.attendance = json.dumps(attendance_obj)
                instance.save()

            except:
                raise exceptions.NotAcceptable('Invalid Date/Time format !')
        else:
            raise serializers.ValidationError("Invalid user details")

        return instance