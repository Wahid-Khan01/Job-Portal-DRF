from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegisterationSerializer, UserLoginSerializer, UserProfileSerializer, UserPersonalInfoSerializer, UserEducationSerializer, UserExperienceSerializer, UserSkillsSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.core.signals import request_finished
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User, PersonalInfo, Education, Experience, Skill, Profile



# Create your views here.

#Generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class TokenObtainView(APIView):
    def post(self, request):
        # Retrieve or create user object
        user = User.objects.get(username=request.data['username'])

        # Generate tokens for the user
        tokens = get_tokens_for_user(user)

        return Response(tokens)
    
class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')  # Get the refresh token from request data

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Attempt to refresh the token
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return Response({'access': new_access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Failed to refresh token'}, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterationView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]
    def post(self,request):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg' : 'Register Successful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Success'}, status = status.HTTP_200_OK)
            else:
                return Response({'errrors':{'non_field_errors':['Email or Password is not valid']}}, status = status.HTTP_404_NOT_FOUND)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPersonalInfoView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, id, format=None):
        user_info = get_object_or_404(PersonalInfo, user=id)
        serializer = UserPersonalInfoSerializer(user_info)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        user = request.user
        existing_info = PersonalInfo.objects.filter(user=user).first()
        if existing_info:
            return Response({'message': 'Personal information already exists for the user'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserPersonalInfoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response({'message': 'Personal information created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, id, format=None):
        user = get_object_or_404(PersonalInfo, user=id)
        serializer = UserPersonalInfoSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Personal information updated successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id , format=None):
        user =PersonalInfo.objects.filter(user=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserEducationView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, id, format=None):
        user_info = get_object_or_404(Education, user=id)
        serializer = UserEducationSerializer(user_info)
        return Response(serializer.data)


    def post(self, request, format=None):
        user = request.user  # Assuming you are using authentication and the user is available in the request
        
        # Check if the user already has an education record
        if Education.objects.filter(user=user).exists():
            return Response({'error': 'Education record already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserEducationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg' :'Education Information Field Successfull'},status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request ,id, format=None):
        user =Education.objects.get(user=id)
        serializer = UserEducationSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' :'Education updated successfully'},status= status.HTTP_201_CREATED)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id , format=None):
        user =Education.objects.get(user=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserExperienceView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, id, format=None):
        user_info = get_object_or_404(Experience, user=id)
        serializer = UserExperienceSerializer(user_info)
        return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user  # Assuming you are using authentication and the user is available in the request
        
        # Check if the user already has an experience record
        if Experience.objects.filter(user=user).exists():
            return Response({'error': 'Experience record already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserExperienceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg' :'Experience Information Field Added Successfull'},status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request ,id, format=None):
        user =Experience.objects.get(user=id)
        serializer = UserExperienceSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' :'Experience updated successfully'},status= status.HTTP_201_CREATED)
        return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id , format=None):
        user =Experience.objects.get(user=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class UserSkillsView(APIView):

    def get(self, request, id, format=None):
        user_info = get_object_or_404(Skill, user=id)
        serializer = UserSkillsSerializer(user_info)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user_id = data.get('user')
        user = get_object_or_404(User, id=user_id)
        
        # Check if the user already has a skill
        existing_skill = Skill.objects.filter(user=user).first()
        if existing_skill:
            return Response({"message": "Skill already exists for the user"})
        
        skill = Skill.objects.create(user=user, skills=data['skills'])
        return Response({"message": "Skill created successfully"})

    def put(self, request, id, format=None):
        skills = Skill.objects.filter(user_id=id)
        if not skills:
            return Response({"message": "Skill does not exist for the user"}, status=400)

        skill = skills.first()
        serializer = UserSkillsSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Skills updated successfully'}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        skills = Skill.objects.filter(user_id=id)
        if not skills:
            return Response({"message": "Skill does not exist for the user"}, status=400)

        skill = skills.first()
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user  # Get the current user

        try:
            profile = Profile.objects.get(user=user)
            personal_info = PersonalInfo.objects.get(user=user)
            education = Education.objects.get(user=user)
            experience = Experience.objects.get(user=user)
            skills = Skill.objects.get(user=user)

            profile_serializer = UserProfileSerializer(profile)
            personal_info_serializer = UserPersonalInfoSerializer(personal_info)
            education_serializer = UserEducationSerializer(education)
            experience_serializer = UserExperienceSerializer(experience)
            skills_serializer = UserSkillsSerializer(skills)

            response_data = {
                'profile': profile_serializer.data,
                'personal_info': personal_info_serializer.data,
                'education': education_serializer.data,
                'experience': experience_serializer.data,
                'skills': skills_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except (Profile.DoesNotExist, PersonalInfo.DoesNotExist, Education.DoesNotExist, Experience.DoesNotExist, Skill.DoesNotExist):
            return Response({'message': 'User profile does not exist'}, status=status.HTTP_404_NOT_FOUND)