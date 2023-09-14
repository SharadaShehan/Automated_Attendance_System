from rest_framework import generics, views, response, status, permissions
from database.models import CustomUser, Role, Company
from .serializers import ExecutiveViewEmployeeSerializer, EmployeeViewEmployeeSerializer, ExecutiveUpdateEmployeeSerializer, EmployeeUpdateEmployeeSerializer, UserLoginSerializer, ExecutiveViewRoleSerializer, ExecutiveCreateRoleSerializer, ExecutiveViewCompanySerializer
from django.contrib.auth import authenticate, login, logout
from .mixins import ProductionAuthentication, DebugSessionAuthentication, DebugFullAuthentication, ViewOnlyOwnCompanyRestriction, ViewOnlyOwnAccountRestriction
from .permissions import ViewOwnAccountPermission, ViewAnyEmployeePermission, EditAnyEmployeePermission, ViewAllEmployeesPermission, ViewAnyRolePermission, ViewAllRolesPermission, ViewOwnCompanyPermission, DeleteOwnCompanyPermission, DeleteAnyRolePermission


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
    serializer_class = ExecutiveViewEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, ViewAllEmployeesPermission]

    def get_queryset(self):
        return CustomUser.objects.filter(company=self.request.user.company)

class ExecutiveUpdateEmployeeView(SetAuthenticationMethod, generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ExecutiveUpdateEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, EditAnyEmployeePermission]

class ExecutiveDeleteEmployeeView(SetAuthenticationMethod, generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ExecutiveViewEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, EditAnyEmployeePermission]



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
                return response.Response({'message': f'Welcome, {user.first_name}!', 'style_guide': user.company.style_guide}, status=status.HTTP_200_OK)
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
    serializer_class = ExecutiveViewRoleSerializer
    permission_classes = [permissions.IsAuthenticated, ViewAllRolesPermission]

    def get_queryset(self):
        return Role.objects.filter(company=self.request.user.company)

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



# CRUD operations for Company Table

class ExecutiveViewCompanyView(SetAuthenticationMethod, ViewOnlyOwnCompanyRestriction, generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = ExecutiveViewCompanySerializer
    permission_classes = [permissions.IsAuthenticated, ViewOwnCompanyPermission]

class ExecutiveUpdateCompanyView(SetAuthenticationMethod, ViewOnlyOwnCompanyRestriction, generics.UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = ExecutiveViewCompanySerializer
    permission_classes = [permissions.IsAuthenticated, ViewOwnCompanyPermission]

class ExecutiveDeleteCompanyView(SetAuthenticationMethod, ViewOnlyOwnCompanyRestriction, generics.DestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = ExecutiveViewCompanySerializer
    permission_classes = [permissions.IsAuthenticated, DeleteOwnCompanyPermission]


