from rest_framework import generics, views, response, status, permissions
from database.models import CustomUser, Role
from .serializers import ExecutiveViewEmployeeSerializer, EmployeeViewEmployeeSerializer, ExecutiveUpdateEmployeeSerializer, EmployeeUpdateEmployeeSerializer, UserLoginSerializer, ExecutiveViewRoleSerializer, ExecutiveCreateRoleSerializer
from django.contrib.auth import authenticate, login, logout
from .mixins import ProductionAuthentication, DebugSessionAuthentication, DebugFullAuthentication, ViewOnlyOwnAccountRestriction
from .permissions import ViewOwnAccountPermission, ViewAnyEmployeePermission, EditAnyEmployeePermission, ViewAllEmployeesPermission, ViewAnyRolePermission, ViewAllRolesPermission, DeleteAnyRolePermission
import re, json

class SetAuthenticationMethod(DebugFullAuthentication): pass


# CRUD operations for Employee Table

class EmployeeViewEmployeeView(ViewOnlyOwnAccountRestriction, SetAuthenticationMethod, generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = EmployeeViewEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, ViewOwnAccountPermission]

class EmployeeUpdateEmployeeView(ViewOnlyOwnAccountRestriction, SetAuthenticationMethod, generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = EmployeeUpdateEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, ViewOwnAccountPermission]

class ExecutiveViewEmployeeView(SetAuthenticationMethod, generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ExecutiveViewEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, ViewAnyEmployeePermission]

class ExecutiveListViewEmployeeView(SetAuthenticationMethod, generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ExecutiveViewEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, ViewAllEmployeesPermission]

    # def get_queryset(self):
    #     return CustomUser.objects.filter(company=self.request.user.company)

class ExecutiveUpdateEmployeeView(SetAuthenticationMethod, generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ExecutiveUpdateEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, EditAnyEmployeePermission]

class ExecutiveDeleteEmployeeView(SetAuthenticationMethod, generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ExecutiveViewEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, EditAnyEmployeePermission]

# View Attendance
class ExecutiveViewAttendanceView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, ViewAnyEmployeePermission]

    def get(self, request, *args, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')
        if not year or not month or not day:
            return response.Response({'message': 'Invalid URL'}, status=status.HTTP_400_BAD_REQUEST)
        if not self.validate_date(year, month, day):
            return response.Response({'message': 'Invalid date'}, status=status.HTTP_400_BAD_REQUEST)
        users = CustomUser.objects.all()
        attendances = []
        for user in users:
            attendance_dict = json.loads(user.attendance)
            if attendance_dict.get(year):
                if attendance_dict[year].get(month):
                    if attendance_dict[year][month].get(day):
                        attendance = attendance_dict[year][month][day]
                        attendance['id'] = user.id
                        attendance['first_name'] = user.first_name
                        attendance['last_name'] = user.last_name
                        attendances.append(attendance)
                        continue
            attendance = {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'entrance': [], 'leave': []}
            attendances.append(attendance)
        return response.Response(attendances, status=status.HTTP_200_OK)

    def validate_date(self, year, month, day):
        if re.match(r'^\d{4}$', year):
            if re.match(r'^\d{2}$', month) and int(month) in range(1, 13):
                if re.match(r'^\d{2}$', day) and int(day) in range(1, 32):
                    return True


# User Authentication

class UserLoginView(views.APIView):
    def post(self, request):
        if request.user.id:
            return response.Response({'message': f'You have already logged in as, {request.user.first_name}'}, status=status.HTTP_200_OK)
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return response.Response({'message': f'Welcome, {user.first_name}!'}, status=status.HTTP_200_OK)
            else:
                return response.Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(SetAuthenticationMethod, views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        logout(request)
        return response.Response({'message': 'Logout successful!'}, status=status.HTTP_200_OK)



# CRUD operations for Role Table

class ExecutiveViewRoleView(SetAuthenticationMethod, generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = ExecutiveViewRoleSerializer
    permission_classes = [permissions.IsAuthenticated, ViewAnyRolePermission]

class ExecutiveListViewRoleView(SetAuthenticationMethod, generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = ExecutiveViewRoleSerializer
    permission_classes = [permissions.IsAuthenticated, ViewAllRolesPermission]

    # def get_queryset(self):
    #     return Role.objects.filter(company=self.request.user.company)

class ExecutiveCreateRoleView(SetAuthenticationMethod, generics.CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = ExecutiveCreateRoleSerializer
    permission_classes = [permissions.IsAuthenticated, ViewAllRolesPermission]

class ExecutiveUpdateRoleView(SetAuthenticationMethod, generics.UpdateAPIView):
    queryset = Role.objects.all()
    serializer_class = ExecutiveViewRoleSerializer
    permission_classes = [permissions.IsAuthenticated, ViewAnyRolePermission]

class ExecutiveDeleteRoleView(SetAuthenticationMethod, generics.DestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = ExecutiveViewRoleSerializer
    permission_classes = [permissions.IsAuthenticated, DeleteAnyRolePermission]





