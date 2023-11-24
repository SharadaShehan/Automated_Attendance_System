from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from .serializers import LoginSerializer, UserRegistrationSerializer, UserUpdateSerializer, UserDetailSerializer
from .models import CustomUser

class CustomLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:    # If username and password are valid(match)
                login(request, user)
                #  !!! Below response is where, user must be redirected, if login in is successful
                # next_path = request.data.get('next')
                next_path =  request.data.get('next')
                if next_path:   # 'next' was sent through same json object, which contains username and password
                    return redirect(next_path)
                return Response({'message': f'Welcome, {user.username}!'}, status=status.HTTP_200_OK)

            else:       # If username and password are invalid(do not match)
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLogoutView(APIView):
    def get(self, request):
        logout(request)
        #  !!! Below response is where, user must be redirected, when he is logged out
        return Response({'message': 'Logout successful!'}, status=status.HTTP_200_OK)


class SignUpView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Login the user after successful registration
            login(request, user)
            return Response({'message': 'SignUp successful!'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountUpdateView(APIView):
    def patch(self, request):
        user = request.user  # Get the currently authenticated user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            login(request, user)
            return Response({'message': 'Account details updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDeleteView(APIView):
    def delete(self, request):
        user = request.user  # Get the currently authenticated user
        user.delete()  # Delete the user account
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



class AccountRetrieveViewByNonOwner(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer

class AccountListViewByNonOwner(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer

class AccountCreateViewByNonOwner(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

class AccountUpdateViewByNonOwner(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer

class AccountDeleteViewByNonOwner(generics.RetrieveDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer




# class AccountCreateViewByNonOwner(APIView):
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({'message': 'Account Created successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AccountUpdateViewByNonOwner(APIView):
#     def patch(self, request, pk):
#         try:
#             user = CustomUser.objects.get(pk=pk)
#         except CustomUser.DoesNotExist:
#             return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         # Check if the authenticated user has permission to update another user's account
#         if request.user.is_superuser:
#             serializer = UserUpdateSerializer(user, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({'message': 'Account details updated successfully'}, status=status.HTTP_200_OK)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'message': 'You do not have permission to update this account'}, status=status.HTTP_403_FORBIDDEN)


# class AccountDeleteViewByNonOwner(APIView):
#     def delete(self, request, pk):
#         try:
#             user = CustomUser.objects.get(pk=pk)
#         except CustomUser.DoesNotExist:
#             return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         # Check if the authenticated user has permission to delete another user's account
#         if request.user.is_superuser:
#             user.delete()  # Delete the user account
#             return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({'message': 'You do not have permission to delete this account'}, status=status.HTTP_403_FORBIDDEN)