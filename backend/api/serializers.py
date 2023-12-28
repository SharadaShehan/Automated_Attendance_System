from database.models import CustomUser, Role
from rest_framework import serializers


class ExecutiveViewEmployeeSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()
    has_read_permission = serializers.SerializerMethodField()
    has_edit_permission = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role_name', 'has_read_permission', 'has_edit_permission', 'first_name', 'last_name', 'picture',
                  'attendance']

    def get_role_name(self, obj):
        try:
            return Role.objects.get(id=obj.role.id).name
        except Role.DoesNotExist:
            return None

    def get_has_read_permission(self, obj):
        try:
            return Role.objects.get(id=obj.role.id).has_read_permission
        except Role.DoesNotExist:
            return None

    def get_has_edit_permission(self, obj):
        try:
            return Role.objects.get(id=obj.role.id).has_edit_permission
        except Role.DoesNotExist:
            return None


class EmployeeViewEmployeeSerializer(ExecutiveViewEmployeeSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role_name', 'has_read_permission', 'has_edit_permission', 'first_name', 'last_name', 'picture',
                  'attendance', 'notifications']


class EmployeeUpdateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        read_only_fields = ['email', 'password', 'role', 'attendance']
        fields = ['first_name', 'last_name', 'picture', 'notifications']

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
        read_only_fields = ['id', 'password', 'notifications', 'picture', 'email', 'first_name', 'last_name']
        fields = ['id', 'role', 'role_name', 'has_read_permission', 'has_edit_permission', 'attendance']


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class ExecutiveViewRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'has_read_permission', 'has_edit_permission' ]

class ExecutiveCreateRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'has_read_permission', 'has_edit_permission' ]

    # def create(self, validated_data):
    #     request = self.context.get('request', None)
    #     if request and request.user.id:
    #         company = request.user.company
    #         validated_data['company'] = company
    #     else:
    #         raise serializers.ValidationError("Login with a authorized account")
    #     return super().create(validated_data)


