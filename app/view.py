from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers,status
from .models import User,Team 
from rest_framework.response import Response

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
    
class EnterTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","team"]
class EnterTeamView(ModelViewSet):
    queryset = User.objects
    serializer_class = EnterTeamSerializer
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        new_team_id = serializer.validated_data.get('team').id
        if new_team_id:
            new_team = Team.objects.get(pk=new_team_id)
            if new_team.user_set.count() >= 4:
                return Response({"error": "队伍已满四人"}, status=status.HTTP_400_BAD_REQUEST)
            if instance.team:
                return Response({"error": "已在一个队伍中"}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer.save()
        return Response(serializer.data)
    
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