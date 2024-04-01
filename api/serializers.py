from rest_framework import serializers
from .models import User, PersonalInfo, Education, Experience, Skill, Profile



class UserRegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }

    #validating password and confirm password while registration

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password does not match')
        return attrs 

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserPersonalInfoSerializer(serializers.ModelSerializer):
  class Meta:
    model = PersonalInfo
    fields='__all__'

class UserEducationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Education
    fields='__all__'

class UserExperienceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Experience
    fields='__all__'


class UserSkillsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Skill
    fields='__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"