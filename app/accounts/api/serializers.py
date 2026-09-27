
from django.contrib.auth import get_user_model
from rest_framework import serializers
User= get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","password","first_name","last_name"]
        extra_kwargs={
            "password":{"write_only":True}
        
        }
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","first_name","last_name"]
