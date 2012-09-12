import urllib2
from xml.dom import minidom
from datetime import datetime as DateTime
from datetime import date, timedelta
import datetime
import pytz
import sys

from importGames import ImportGamesCron
from tigsOnTop import settings
from gameTracker.models import Game

lineClear = "***************************************"

class UpdateGameCron(ImportGamesCron):

    TIMEZONE = pytz.timezone(settings.TIME_ZONE)
    START_UPDATING_PREGAME_HOURS = 1
    UPDATE_BEYOND_MIDNIGHT_HOURS = 8

    def updateGame(self):
        print "updating game"
        if self.isGameActive():
            print lineClear
            print "game is active"
            self.updateActiveGame()

    def isGameActive(self):
        minQueryTime = self.TIMEZONE.localize(
            datetime.datetime.today() - timedelta(
                hours=self.START_UPDATING_PREGAME_HOURS))
        maxQueryTime = self.timezone.localize(
            datetime.datetime.today() + timedelta(
                hours=self.UPDATE_BEYOND_MIDNIGHT_HOURS))
        
        activeGames = Game.objects.filter(startTime__range=(minQueryTime, maxQueryTime))
        activeGames.exclude(currentStatus="FINAL")
        
        if len(activeGames) > 0:
            return True
        else:
            return False
    
    def updateActiveGame(self):
        localToday = self.TIMEZONE.localize(datetime.datetime.today())
        activeGames = self.getGamesToImportByDay(localToday)
        activeGame = activeGames[0]
        print activeGame
        activeGame.save()
        

if __name__ == "__main__":
    updater = UpdateGameCron()
    updater.updateGame()
