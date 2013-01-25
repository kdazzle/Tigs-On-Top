import datetime
import pytz

from django.db import models
from tigsOnTop import settings

__author__ = "Kyle Valade"

class Game(models.Model):
    TIMEZONE = pytz.timezone(settings.TIME_ZONE)

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

    def importNewGame(self):
        matchingGames = Game.objects.filter(startTime=self.startTime)
        if len(matchingGames) == 0:
            super(Game, self).save()

    def getLocalizedStartTime(self):
        locTime = self.startTime.astimezone(self.TIMEZONE)
        return locTime
