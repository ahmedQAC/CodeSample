from rest_framework import generics
from rest_framework.response import Response
from .mixins import IsOrganiserQuerysetMixin
from .models import Session
from .serializers import (SessionSerializer,
                          SessionUpdateSerializer,
                          SessionCancelSerializer,
                          SessionHostedSerializer,
                          SessionViewSerializer)


class SessionCreateAPIView(generics.CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def perform_create(self, serializer):
        number_of_teams = serializer.validated_data.pop('number_of_teams', '')
        maximum_players_per_team = serializer.validated_data.pop('maximum_players_per_team', '')
        instance = serializer.save(organiser=self.request.user)

        if number_of_teams and maximum_players_per_team:
            instance.create_standby_and_team_objects(
                number_of_teams=number_of_teams,
                maximum_players_per_team=maximum_players_per_team
            )


class SessionUpdateAPIView(IsOrganiserQuerysetMixin, generics.UpdateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionUpdateSerializer
    user_field = 'organiser'
    allow_staff_view = False

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.has_ended():
            return Response({'detail': 'Can not update session, it has ended'})
        return super().update(request, *args, **kwargs)


class SessionCancelAPIView(IsOrganiserQuerysetMixin, generics.UpdateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionCancelSerializer


class SessionAllAPIView(generics.ListAPIView):
    """Get a list of all Sessions that requested user has joined and hosted"""
    queryset = Session.objects.all()
    serializer_class = SessionHostedSerializer

    def get_queryset(self):
        user = self.request.user
        all_active_qs = self.queryset.all_active(user)
        all_inactive_qs = self.queryset.all_inactive(user)
        combined_qs = all_active_qs | all_inactive_qs
        return combined_qs


class SessionHostedAPIView(IsOrganiserQuerysetMixin, generics.ListAPIView):
    """Get a list of all Sessions that requested user has hosted"""
    queryset = Session.objects.all()
    serializer_class = SessionHostedSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        active_qs = qs.active()
        inactive_qs = qs.inactive()
        combined_qs = active_qs | inactive_qs
        return combined_qs


class SessionAPIView(generics.RetrieveAPIView):
    """View single Session"""
    queryset = Session.objects.all()
    serializer_class = SessionViewSerializer
