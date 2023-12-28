from database.models import CustomUser, Role, Company
from rest_framework import serializers, exceptions
import json
import face_recognition
import numpy as np
from .ml_model import MLModel
from werkzeug.security import generate_password_hash


class MiddlewareCreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'gender']

    def create(self, validated_data):

        company = Company.objects.get_company()
        if company is None:
            raise exceptions.ValidationError({'message': 'Company does not exist'})
        init_token = self.context['request'].headers.get('Authorization')
        if init_token != company.init_token:
            raise exceptions.ValidationError({'message': 'Invalid init token'})

        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        user.role = Company.objects.get_company().default_role
        user.attendance = '{}'

        if password:
            user.set_password(password)
            user.save()
        else:
            user.delete()
            raise exceptions.ValidationError({'message': 'Password is required'})

        try:
            converted_photo = np.array(self.context['request'].data.get('photo')).astype(np.uint8)
            encodings = face_recognition.face_encodings(converted_photo)[0]
            json_encodings = json.dumps(encodings.tolist())
            user.encodings = json_encodings
            user.save()
            user_data = {'id': user.id,
                         'first_name': user.first_name,
                         'last_name': user.last_name,
                         'gender': user.gender,
                         'encodings': encodings}
            success = MLModel.add_user_encodings(user_data)
            if not success:
                user.delete()
                raise Exception('Failed to add user encodings to queue')
        except Exception as e:
            user.delete()
            raise exceptions.ValidationError({'message': f'{e}'})

        return user


class MiddlewareCreateCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['name', 'username', 'password']

    def create(self, validated_data):
        default_executive_role = Role.objects.create(name='CEO', has_read_permission=True, has_edit_permission=True)
        default_employee_role = Role.objects.create(name='Employee', has_read_permission=False, has_edit_permission=False)
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


