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

class UpdateGameCron(ImportGamesCron):

    TIMEZONE = pytz.timezone(settings.TIME_ZONE)
    START_UPDATING_PREGAME_HOURS = 1
    UPDATE_BEYOND_MIDNIGHT_HOURS = 12

    def updateGame(self):
        if self.isGameActive():
            self.updateActiveGame()

    def isGameActive(self):
        minQueryTime = datetime.datetime.today() - timedelta(
                hours=self.START_UPDATING_PREGAME_HOURS)
        maxQueryTime = datetime.datetime.today() + timedelta(
                hours=self.UPDATE_BEYOND_MIDNIGHT_HOURS)
        activeGames = Game.objects.filter(startTime__range=(minQueryTime, maxQueryTime))
        activeGames.exclude(currentStatus="Final")

        if len(activeGames) > 0:
            return True
        else:
            return False
    
    def updateActiveGame(self):
        activeGames = self.getGamesToImportByDay(datetime.datetime.today())
        activeGame = activeGames[0]
        print activeGames
        activeGame.save()
        

if __name__ == "__main__":
    updater = UpdateGameCron()
    updater.updateGame()
