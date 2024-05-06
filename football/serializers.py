from rest_framework import serializers
from .models import Session


class SessionSerializer(serializers.ModelSerializer):
    number_of_teams = serializers.IntegerField(
        write_only=True, min_value=1, max_value=4
    )
    maximum_players_per_team = serializers.IntegerField(
        write_only=True, min_value=1, max_value=11
    )
    
    class Meta:
        model = Session
        fields = [
            'pk',
            'title',
            'location',
            'start_time',
            'end_time',
            'date',
            'amount_per_person',
            'number_of_teams',
            'maximum_players_per_team'
        ]


class SessionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['title', 'location']


class SessionCancelSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Session
        fields = ['detail']
    
    def get_detail(self, obj):
        # if not hasattr(obj, 'id'):
        #     return None
        # if not isinstance(obj, Session):
        #     return None
        
        if obj.canceled:
            return "Session has already been canceled"
        elif obj.has_ended():
            return "Can not cancel session, it has already ended"
        obj.cancel_session()
        return "Session has been canceled"


class SessionHostedSerializer(SessionSerializer):
    organiser = serializers.CharField(source='organiser.username')
    number_of_joined_players = serializers.SerializerMethodField()
    max_players = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
            view_name='football:view',
            lookup_field='pk',
            read_only=True
    )

    class Meta(SessionSerializer.Meta):
        fields = SessionSerializer.Meta.fields + [
            'organiser',
            'number_of_joined_players',
            'max_players',
            'url'
        ]
    
    def get_number_of_joined_players(self, obj):
        return obj.get_number_of_joined_players()

    def get_max_players(self, obj):
        return obj.get_max_players()


class PlayerInLineSerializer(serializers.Serializer):
    user = serializers.CharField(read_only=True)
    username = serializers.CharField(source='user.username')


class TeamInLineSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    maximum_players = serializers.IntegerField(read_only=True)
    players = PlayerInLineSerializer(source='player_set.all', many=True)


class SessionViewSerializer(SessionSerializer):
    organiser = serializers.CharField(source='organiser.username')
    teams = TeamInLineSerializer(source='team_set.all', many=True)

    class Meta(SessionSerializer.Meta):
        fields = SessionSerializer.Meta.fields + [
            'organiser',
            'teams'
        ]
