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
        todaysDatetime = datetime.datetime.utcnow()
        activeGames = Game.objects.filter(startTime__lte=todaysDatetime).exclude(
            currentStatus=settings.GAME_STATUS_FINAL)
        
        for game in activeGames:
            if game.currentStatus == settings.GAME_STATUS_IN_PROGRESS:
                startTime = game.startTime

        print len(activeGames)
        if len(activeGames) > 0:
            startTime = activeGames[0].startTime
        else:
            startTime = None

        return startTime.astimezone(self.TIMEZONE)

    def updateActiveGames(self, startTime):
        activeGames = self.getGamesToImportByDay(startTime)
        
        #TODO: There should only be one active game at a time...
        for game in activeGames:
            game.save()

if __name__ == "__main__":
    updater = UpdateGameCron()
    updater.updateGame()