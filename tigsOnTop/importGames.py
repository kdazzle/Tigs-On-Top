import urllib2
from xml.dom import minidom
from datetime import datetime as DateTime
import datetime
import pytz
import sys

from django.utils.timezone import utc
from tigsOnTop import settings
from gameTracker.models import Game

class ImportGamesCron():
    TIMEZONE = pytz.timezone(settings.TIME_ZONE)
    IMPORT_ADVANCE_DAYS = settings.IMPORT_ADVANCE_DAYS

    def importGames(self):
        dateRange = self.getDateRange()
        for day in dateRange:
            games = self.getGamesToImportByDay(day)
            self.saveGames(games)

    def getDateRange(self):
        base = self.TIMEZONE.localize(datetime.datetime.today())
        dateList = [
                base + datetime.timedelta(days=x) for x in range(-1, self.IMPORT_ADVANCE_DAYS)
            ]
        return dateList

    def getGamesToImportByDay(self, day):
        """Returns list of games"""
        try:
            gameDataUrl = self.getGameDataUrl(day)
            remoteDataXml = minidom.parse(urllib2.urlopen(gameDataUrl))
            teamList = remoteDataXml.getElementsByTagName('team')
            tigersGamesNodes = self.getGamesFromTeamList(teamList)

            games = []
            for gameNode in tigersGamesNodes:
                games.append(self.getGameData(gameNode, day))
        except urllib2.HTTPError:
            games = []

        return games

    def getGameDataUrl(self, date):
        month = "%02d" % (date.month)
        day = "%02d" % (date.day)
        year = "%02d" % (date.year)
        url = "http://gd2.mlb.com/components/game/mlb/year_%s/month_%s/day_%s/scoreboard.xml" % (year, month, day)

        return url

    def getGamesFromTeamList(self, teamList):
        #TODO: Error check
        games = []
        for team in teamList:
            teamName = team.attributes["name"].value
            if teamName == settings.THE_TEAM:
                games.append(team.parentNode)
        return games

    def saveGames(self, games):
        for game in games:
            game.importNewGame()

    def getGameData(self, gameNode, day):
        teamsXml = gameNode.getElementsByTagName("team")
        game = Game()
        game.startTime = self.getStartTime(gameNode, day)
        game.currentStatus = self.getGameCurrentStatus(gameNode)
        for teamNode in teamsXml:
            currentTeamName = teamNode.attributes["name"].value
            if currentTeamName == settings.THE_TEAM:
                game.usTeam = settings.THE_TEAM
                game.usScore = self.getScoreFromTeamNode(teamNode)
            else:
                game.themTeam = currentTeamName
                game.themScore = self.getScoreFromTeamNode(teamNode)

        return game

    def getStartTime(self, gameNode, day):
        gameDataNode = gameNode.getElementsByTagName("game")[0]
        startTime = gameDataNode.attributes["start_time"].value
        startDay = "%s %s %s" % (day.month, day.day, day.year)
        utcTime = DateTime.strptime("%s %s" % (startDay, startTime), "%m %d %Y %I:%M%p")
        utcTime.replace(tzinfo=utc)

        return utcTime

    def getGameCurrentStatus(self, gameNode):
        gameDataNode = gameNode.getElementsByTagName("game")[0]
        status = gameDataNode.attributes["status"].value
        return status

    def getScoreFromTeamNode(self, teamNode):
        gameStats = teamNode.getElementsByTagName("gameteam")[0]
        #TODO: throw exception if gameStats len != 1?
        return gameStats.attributes["R"].value


if __name__ == "__main__":
    importer = ImportGamesCron()
    importer.importGames()
