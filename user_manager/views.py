from rest_framework.response import Response
from . user_data_validation import validate_user_data
from .serializer import UserSerializer, LoginSerializer, UserRetrieveSerializer
# , LoginSerializer
from rest_framework import status
from django.conf import settings
from .models import CustomUser
from django_ratelimit.decorators import ratelimit  # type: ignore
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail as django_send_mail
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


def send_custom_mail(user_email):
    subject = 'Tourneyhub'
    message = 'Welcome to Tourneyhub!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    try:
        django_send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
@ratelimit(key='ip', rate='5/m', block=True)
@api_view(['POST'])
def create_user(request):
    print("create_user", request.data)
    try:
        if request.method == 'POST':
            validation_check_status = validate_user_data(request.data, 'user-creation')
            print("validation_check_status", validation_check_status)
            if validation_check_status[0] ==  False:
                check_status_response = validation_check_status[1]
                return Response({"message":check_status_response}, status=status.HTTP_406_NOT_ACCEPTABLE)
            _data = request.data
            serializer = UserSerializer(data= _data, many = False)
            if serializer.is_valid():
                user = CustomUser.objects.create(first_name= serializer.validated_data['first_name'], last_name= serializer.validated_data['last_name'],
                                                username = serializer.validated_data['username'], email = serializer.validated_data['email'],
                                                phone = serializer.validated_data['phone'], date_of_birth= serializer.validated_data['date_of_birth'], age= serializer.validated_data['age'])
                user.set_password(_data['password'])
                user.save()
                send_custom_mail(serializer.validated_data['email'])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors)
        return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except:
        return Response(status= status.HTTP_400_BAD_REQUEST)
    

@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['POST'])
def user_login(request):
    try:
        print(request.data)
        if request.method == 'POST':
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid credentials!'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Method Not Allowed!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    except:
        return Response(status= status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_logout(request):
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Succesfully Logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
    try:
        if request.user.is_authenticated:
            user = CustomUser.objects.filter(id=request.user.id).first()
            serializer = UserRetrieveSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials!'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_user(request):
    try:
        if request.user.is_authenticated:
            users = CustomUser.objects.all()
            serializer = UserRetrieveSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials!'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    try:
        if request.method == 'PUT':
            print("Request FILES:", request.FILES)
            _data = request.data
            data = {key: value for key, value in _data.items()}
            print(data, "data")
            validation_check_response = validate_user_data(data, 'user-update')
            print(validation_check_response)
            if validation_check_response[0] ==  False:
                    check_status_response = validation_check_response[1]
                    return Response({"message":check_status_response}, status=status.HTTP_406_NOT_ACCEPTABLE)
            user = get_object_or_404(CustomUser, id=_data['id'])
            if 'profile_picture' in request.FILES:
                print("Yesssssssssssssssssssssssssssss")
                user.image = request.FILES['profile_picture']
            user.first_name = _data['first_name']
            user.last_name = _data['last_name']
            user.username = _data['email']
            user.email = _data['email']
            user.date_of_birth = _data['date_of_birth']
            user.phone = _data['phone']
            user.age = _data['age']
            user.save()
            return Response({'message': 'Updated succesfully!'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)