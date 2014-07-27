import pytz

from django.db import models
from django.conf import settings


# Game Statuses
GAME_STATUS_IN_PROGRESS = "IN_PROGRESS"
GAME_STATUS_FINAL = "FINAL"
GAME_STATUS_DELAYED = "DELAYED"


class Game(models.Model):
    TIMEZONE = pytz.timezone(settings.TIME_ZONE)

    mlbId = models.CharField(max_length=128, default="")  # TODO: Should be unique!
    usTeam = models.CharField(max_length=64, default=settings.THE_TEAM)
    themTeam = models.CharField(max_length=64)
    usScore = models.IntegerField(default=0)
    themScore = models.IntegerField(default=0)
    startTime = models.DateTimeField()
    addDate = models.DateTimeField(auto_now_add=True)
    currentStatus = models.CharField(max_length=24, blank=True, null=True)

    def __str__(self):
        return """
            usTeam: %s
            usScore: %s
            themTeam: %s
            themScore: %s
            startTime: %s
            currentStatus: %s""" % (self.usTeam,
                self.usScore, self.themTeam, self.themScore,
                self.startTime, self.currentStatus)

    def getLocalizedStartTime(self):
        locTime = self.startTime.astimezone(self.TIMEZONE)
        return locTime

    def get_start_date(self):
        """
        :return {date}: the date on which the game starts
        """
        return self.startTime.date()

    def is_finished(self):
        """Is the game finished?"""
        return self.currentStatus == settings.GAME_STATUS_FINAL
