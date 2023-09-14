from database.models import CustomUser, Role, Company
from rest_framework import serializers, exceptions
from random import randint
import json


with open('./middleware_api/api_code_range.txt', 'r') as file:
    start_value = int(file.readline().strip())
    end_value = int(file.readline().strip())
if not  (int(start_value) and int(end_value)) :
    raise Exception('api_code range is invalid')

class MiddlewareCreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'user_api_code', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        company = self.get_company(); role = self.get_role(); user_api_code = self.get_user_api_code()
        user = super().create(validated_data)
        user.company = company;  user.role = role;  user.user_api_code = user_api_code;  user.attendance = '{}'
        if password:
            user.set_password(password)
            user.save()
        return user

    def get_company(self):
        try:
            return Company.objects.get(company_api_code=self.context['request'].data.get('company_api_code'))
        except Company.DoesNotExist:
            raise serializers.ValidationError("Company doesn't exist")

    def get_role(self):
        try:
            company = Company.objects.get(company_api_code=self.context['request'].data.get('company_api_code'))
            return Role.objects.get(default_key=company.default_role_key)
        except Role.DoesNotExist:
            raise serializers.ValidationError("Role does not exist")

    def get_user_api_code(self):
        while True:
            value = randint(start_value, end_value)
            queryset = CustomUser.objects.filter(user_api_code=value).all()
            if not queryset.exists():
                return value


class MiddlewareCreateCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['name', 'logo', 'style_guide','company_api_code', 'default_executive_id' , 'default_executive_api_code']

    def create(self, validated_data):
        default_key = self.get_default_role_key()
        company = Company.objects.create(name= validated_data.get('name'),
                                         logo= validated_data.get('logo'),
                                         style_guide= validated_data.get('style_guide'),
                                         company_api_code= self.get_company_api_code(),
                                         default_role_key= default_key)
        default_employee_role = Role.objects.create(name='Employee', is_manager=False, is_executive=False, company=company, default_key=default_key)
        default_executive_role = Role.objects.create(name='Executive', is_manager=True, is_executive=True, company= company)
        default_executive_account = self.context['request'].data.get('default_executive_account')

        try:
            default_executive = CustomUser.objects.create(email= default_executive_account['email'] ,
                                                          password= default_executive_account['password'],
                                                          company= company,
                                                          role= default_executive_role,
                                                          user_api_code= self.get_executive_api_code(),
                                                          first_name= default_executive_account['first_name'],
                                                          last_name= default_executive_account['last_name'],
                                                          picture=None,
                                                          attendance = '{}')
            default_executive.set_password(default_executive_account['password'])
            default_executive.save()
            company.default_executive_api_code = default_executive.user_api_code
            company.default_executive_id = default_executive.id
            company.save()
        except Exception as ex:
            Company.objects.filter(id=company.id).delete()
            raise serializers.ValidationError("Invalid User Account Details")

        return company

    def get_company_api_code(self):
        while True:
            value = randint(start_value, end_value)
            queryset = Company.objects.filter(company_api_code=value).all()
            if not queryset.exists():
                return value

    def get_default_role_key(self):
        while True:
            value = randint(start_value, end_value)
            queryset = Role.objects.filter(default_key=value).all()
            if not queryset.exists():
                return value

    def get_executive_api_code(self):
        while True:
            value = randint(start_value, end_value)
            queryset = CustomUser.objects.filter(user_api_code=value).all()
            if not queryset.exists():
                return value


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