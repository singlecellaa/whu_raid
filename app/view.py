from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import serializers,status
from .models import User,Team 
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.models import Token

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","name","student_id","college","password"]
class RegisterView(ModelViewSet):
    queryset = User.objects
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()


class LoginSerializer(serializers.Serializer):
    student_id = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        student_id = attrs.get('student_id')
        password = attrs.get('password')
        try:
            user = User.objects.get(student_id=student_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")
        attrs['user'] = user
        return attrs

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]  # Allow login for anyone

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","name","student_id","college"]
class UserView(ModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer
    
class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = ["id","name","leader_id","members"]
    def get_members(self,obj):
        members_ = obj.user_set.all()
        return UserSerializer(members_,many=True).data
class TeamView(ModelViewSet):
    queryset = Team.objects
    serializer_class = TeamSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = serializer.save()
        try:
            leader = User.objects.get(student_id=team.leader_id)
        except User.DoesNotExist:
            return Response({"error": "404 not found"}, status=status.HTTP_404_NOT_FOUND)
        if leader.team:
            return Response({"error":"已经在一个队伍中"},status=status.HTTP_400_BAD_REQUEST)
        try:
            leader.team = team
            leader.save()
        except Exception as e:
            return Response({"error": f"Failed to add leader to team: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
class EnterTeamSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    team_name = serializers.CharField()
class EnterTeamView(APIView):
    def put(self, request, *args, **kwargs):
        serializer = EnterTeamSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            team_name = serializer.validated_data['team_name']
            try:
                user = User.objects.get(pk=user_id)
                team = Team.objects.get(name=team_name)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except Team.DoesNotExist:
                return Response({"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)

            if team.user_set.count() >= 4:
                return Response({"error": "Team is full"}, status=status.HTTP_400_BAD_REQUEST)
            if user.team:
                return Response({"error": "User is already in a team"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user.team = team
                user.save()
                return Response({"message": "User added to team successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Failed to add user to team: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuitTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'team']
class QuitTeamView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = QuitTeamSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        team = instance.team
        if team:
            if team.leader_id == instance.student_id:
                return Response({"error": "队长不允许退出队伍"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                instance.team = None
                instance.save()
                return Response(serializer.data)
        else:
            return Response({"error": "用户不在任何队伍中"}, status=status.HTTP_400_BAD_REQUEST)


class ReserveStartTimeSerializer(serializers.ModelSerializer):
    reservation_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta: 
        model = Team
        fields = ['id','reservation_time']
class ReserveStartTimeView(ModelViewSet):
    queryset = Team.objects
    serializer_class = ReserveStartTimeSerializer
    
    
class StartTimeSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = Team
        fields = ['id','start_time']
class StartTimeView(ModelViewSet):
    queryset = Team.objects
    serializer_class = StartTimeSerializer
    
    
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id','position']
class PositionView(ModelViewSet):
    queryset = Team.objects
    serializer_class = PositionSerializer