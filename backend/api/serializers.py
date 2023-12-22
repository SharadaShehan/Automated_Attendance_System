from database.models import CustomUser, Role
from rest_framework import serializers


class ExecutiveViewEmployeeSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()
    is_manager = serializers.SerializerMethodField()
    is_executive = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role_name', 'is_manager', 'is_executive', 'first_name', 'last_name', 'picture',
                  'attendance']

    def get_role_name(self, obj):
        try:
            return Role.objects.get(id=obj.role.id).name
        except Role.DoesNotExist:
            return None

    def get_is_manager(self, obj):
        try:
            return Role.objects.get(id=obj.role.id).is_manager
        except Role.DoesNotExist:
            return None

    def get_is_executive(self, obj):
        try:
            return Role.objects.get(id=obj.role.id).is_executive
        except Role.DoesNotExist:
            return None


class EmployeeViewEmployeeSerializer(ExecutiveViewEmployeeSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role_name', 'is_manager', 'is_executive', 'first_name', 'last_name', 'picture',
                  'attendance', 'notifications']


class EmployeeUpdateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        read_only_fields = ['company', ' user_api_code', 'role', 'email', 'attendance', 'password' ]
        fields = ['first_name', 'last_name', 'picture', 'email_notifications' ]

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        current_password = self.context['request'].data.get('current_password', None)
        new_password = self.context['request'].data.get('new_password', None)
        if current_password and new_password:
            if instance.check_password(current_password):
                instance = super().update(instance, validated_data)
                instance.set_password(new_password)
                instance.save()
            else:
                raise serializers.ValidationError("wrong password")
            return instance
        else:
            return super().update(instance, validated_data)


class ExecutiveUpdateEmployeeSerializer(ExecutiveViewEmployeeSerializer):
    class Meta:
        model = CustomUser
        read_only_fields = ['id', 'password', 'notifications', 'picture']
        fields = ['id', 'email', 'role', 'role_name', 'is_manager', 'is_executive', 'first_name', 'last_name',
                  'attendance']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class ExecutiveViewRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'is_manager', 'is_executive' ]

class ExecutiveCreateRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'is_manager', 'is_executive' ]

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and request.user.id:
            company = request.user.company
            validated_data['company'] = company
        else:
            raise serializers.ValidationError("Login with a authorized account")
        return super().create(validated_data)


