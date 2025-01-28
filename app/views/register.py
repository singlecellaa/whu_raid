from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from ..models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name","student_id","college"]
        
class RegisterView(ModelViewSet):
    queryset = User.objects
    serializer_class = RegisterSerializer