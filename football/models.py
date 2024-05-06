import uuid
import datetime

from django.db import models
from django.db.models import Q, Sum
from django.conf import settings
from django.core.validators import (MinValueValidator)
from django.utils import timezone
from decimal import Decimal


class SessionQuerySet(models.QuerySet):
    def hosted(self, user):
        """Returns a qs of sessions that the user has organised."""
        return self.filter(organiser=user)

    def guest(self, user):
        """Returns a qs of sessions that user has been a part of."""
        return self.filter(player__user=user).exclude(organiser=user)

    def active(self):
        """Returns a qs of active sessions."""
        active_qs = self.filter(
            Q(date__gte=datetime.date.today(), start_time__gt=datetime.datetime.now()) |
            Q(date__gt=datetime.date.today())
        ).order_by('date')
        return active_qs

    def inactive(self):
        """Returns a qs of inactive (in the past) sessions."""
        inactive_qs = self.filter(
            Q(date__lte=datetime.date.today(), start_time__lte=datetime.datetime.now()) |
            Q(date__lt=datetime.date.today())
        ).order_by('-date')
        return inactive_qs

    def all_active(self, user):
        """Returns qs of all active sessions for given user"""
        hosted_qs = self.hosted(user).active()
        guest_qs = self.guest(user).active()
        combined_qs = hosted_qs | guest_qs
        return combined_qs
    
    def all_inactive(self, user):
        """Returns qs of all inactive sessions for given user"""
        hosted_qs = self.hosted(user).inactive()
        guest_qs = self.guest(user).inactive()
        combined_qs = hosted_qs | guest_qs
        return combined_qs


# class SessionManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         return SessionQuerySet(self.model, using=self._db)


class Session(models.Model):
    title = models.CharField(max_length=100)
    organiser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=False, null=False)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    invitation_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    private_session = models.BooleanField(default=True)
    amount_per_person = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('1.0'))])
    collect_payments = models.BooleanField(default=False)
    players_can_change_team = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)

    # objects = SessionManager()
    objects = SessionQuerySet().as_manager()

    def has_ended(self):
        """Method to check if the session has ended.

        Returns True if current date and time is greater than self.date
        and self.end_time, and returns False otherwise."""
        todays_date = timezone.now()
        naive_session_datetime = datetime.datetime.combine(
            self.date, self.end_time
        )
        # https://stackoverflow.com/a/36623787
        aware_session_datetime = timezone.make_aware(naive_session_datetime)
        if todays_date < aware_session_datetime:
            return False
        return True

    def cancel_session(self):
        """Method to 'Cancel' a session"""
        # Refund all players (PaymentIntent)
        # Cancel organiser payout celery_task
        self.canceled = True
        self.save()
        return True

    def create_standby_and_team_objects(self, number_of_teams=2, maximum_players_per_team=5):
        """Creates a Standby object and Team objects specified
        by number_of_teams"""

        Standby.objects.create(
            session=self
        )

        for i in range(1, number_of_teams + 1):
            Team.objects.create(
                session=self,
                name=f'Team {i}',
                # colour='Dark',
                maximum_players=maximum_players_per_team
            )

    def get_number_of_joined_players(self):
        """Returns the number of players that have joined any time for
        this session."""
        number_of_players = Player.objects.filter(session=self).count()
        return number_of_players

    def get_max_players(self):
        """Returns maximum players for a session by using number of teams and
        Team.maximum_players. This doesn not include players in Standby"""
        sum_dict = Team.objects.filter(session=self).aggregate(Sum('maximum_players'))
        return sum_dict['maximum_players__sum']


class Team(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    allow_player_addition = models.BooleanField(default=True)
    # colour = models.CharField(max_length=20)
    maximum_players = models.PositiveSmallIntegerField(default=11)


class Standby(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


class Player(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    standby = models.ForeignKey(Standby, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)