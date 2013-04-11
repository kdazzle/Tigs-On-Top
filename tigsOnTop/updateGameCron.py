#!/usr/local/bin/python2.7
import urllib2
from xml.dom import minidom
from datetime import datetime as DateTime
from datetime import date, timedelta
import datetime
import pytz
import sys

from django.utils.timezone import utc
from importGames import ImportGamesCron
from tigsOnTop import settings
from gameTracker.models import Game

lineClear = "***************************************"

class UpdateGameCron(ImportGamesCron):

    TIMEZONE = pytz.timezone(settings.TIME_ZONE)
    START_UPDATING_PREGAME_HOURS = 1
    UPDATE_BEYOND_MIDNIGHT_HOURS = 8

    def updateGame(self):
        startTimeOfTodaysGame = self.getStartTimeOfTodaysGame()
        if startTimeOfTodaysGame is not None:
            self.updateActiveGames(startTimeOfTodaysGame)
    
    def getStartTimeOfTodaysGame(self):
        nowTime = datetime.datetime.utcnow()
        midniteTonite = datetime.datetime.now(pytz.timezone("America/Detroit")) \
		.replace(hour=0, minute=0, second=0, microsecond=0) \
		.astimezone(pytz.utc)
        activeGames = Game.objects.filter(startTime__lte=nowTime, startTime__gte=midniteTonite).exclude(
            currentStatus=settings.GAME_STATUS_FINAL)
        
        for game in activeGames:
            startTime = game.startTime

        if len(activeGames) > 0:
            startTime = activeGames[0].startTime
        else:
            return None

        return startTime.astimezone(self.TIMEZONE)

    def updateActiveGames(self, startTime):
        activeGames = self.getGamesToImportByDay(startTime)
        
        #TODO: There should only be one active game at a time...
        for game in activeGames:
            existingGame = Game.objects.filter(startTime=game.startTime)[0]
            existingGame = self.updateExistingGameFields(existingGame, game)
            existingGame.save()

    def updateExistingGameFields(self, existingGame, newGame):
        existingGame.usScore = newGame.usScore
        existingGame.themScore = newGame.themScore
        existingGame.currentStatus = newGame.currentStatus
        return existingGame

if __name__ == "__main__":
    updater = UpdateGameCron()
    updater.updateGame()
