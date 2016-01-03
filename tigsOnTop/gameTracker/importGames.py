import os
import urllib2
from xml.dom import minidom
from datetime import datetime as DateTime
import datetime
from logging import getLogger

import pytz
from django.utils.timezone import utc

from tigsOnTop import settings
from .models import Game


l = getLogger(__name__)


class ImportGamesCron():
    TIMEZONE = pytz.timezone(settings.TIME_ZONE)
    IMPORT_ADVANCE_DAYS = settings.IMPORT_ADVANCE_DAYS

    def importGames(self):
        dateRange = self.getDateRange()
        for day in dateRange:
            games = self.getGamesFromMlbForDay(day)
            self.saveGames(games)

    def getDateRange(self):
        base = self.TIMEZONE.localize(datetime.datetime.today())
        dateList = [
            base + datetime.timedelta(days=x) for x in range(-1, self.IMPORT_ADVANCE_DAYS)
        ]
        return dateList

    def getGamesFromMlbForDay(self, day):
        """
        Retrieve a list of Tigers games from the MLB API for a given date

        :param date day: date of a game
        :return list list of Tigers games
        """
        try:
            gameDataUrl = self.getGameDataUrl(day)
            remoteDataXml = minidom.parseString(urllib2.urlopen(gameDataUrl))
            teamList = remoteDataXml.getElementsByTagName('team')  # List of games by team
            tigersGamesNodes = self._filterForTigersGames(teamList)

            games = []
            for gameNode in tigersGamesNodes:
                games.append(self._createGameFromXml(gameNode, day))
        except urllib2.HTTPError:
            l.exception("Unable to retrieve games from MLB API")
            games = []

        return games

    def getGameDataUrl(self, date):
        """
        Get the URL of the XML file of a day's games

        :param date date: get the baseball games for this date
        :return string: the url
        """
        month = "%02d" % (date.month)
        day = "%02d" % (date.day)
        year = "%02d" % (date.year)
        url = "http://gd2.mlb.com/components/game/mlb/year_%s/month_%s/day_%s/scoreboard.xml" % (year, month, day)

        return url

    def _filterForTigersGames(self, teamList):
        """
        Return a list of games in which the Tigers are playing.

        :param list teamList: list of team nodes. Team nodes are children of
         game nodes.
        :return list: list of xml game nodes
        """
        #TODO: Error check
        games = []
        for team in teamList:
            teamName = team.attributes["name"].value
            if teamName == settings.THE_TEAM:
                games.append(team.parentNode)
        return games

    def saveGames(self, games):
        """
        Saves each game if it isn't already in the database

        :param list games: list of Games
        """
        for game in games:
            matchingGames = Game.objects.filter(startTime=game.startTime)
            if len(matchingGames) == 0:
                game.save()

    def _createGameFromXml(self, gameNode, day):
        """
        Convert the xml representation of a game into a `Game` object, but
        don't persist it to the database.

        :param gameNode: the xml data of a game
        :param date day: the date of the game. Need it to create a datetime
         from the xml data.
        :return Game:
        """
        teamsXml = gameNode.getElementsByTagName("team")
        gameDataNode = gameNode.getElementsByTagName("game")[0]
        gameAttributes = gameDataNode.attributes

        game = Game()
        game.startTime = self._getStartTime(
            gameAttributes['start_time'].value, day)
        game.currentStatus = gameAttributes['status'].value
        game.mlbId = gameAttributes['id'].value
        for teamNode in teamsXml:
            currentTeamName = teamNode.attributes["name"].value
            if currentTeamName == settings.THE_TEAM:
                game.usTeam = settings.THE_TEAM
                game.usScore = int(self._getScoreFromTeamNode(teamNode))
            else:
                game.themTeam = currentTeamName
                game.themScore = int(self._getScoreFromTeamNode(teamNode))

        return game

    def _getStartTime(self, startTime, day):
        """
        Create the datetime of a given game using the given `day` and the
        time given in the xml.

        :param gameNode: the XML attribute representing the game's start
        :param date day: the day of the game
        :return datetime:
        """
        startDay = "%s %s %s" % (day.month, day.day, day.year)
        utcTime = DateTime.strptime("%s %s" % (startDay, startTime), "%m %d %Y %I:%M%p")
        utcTime.replace(tzinfo=utc)

        return utcTime

    def _getScoreFromTeamNode(self, teamNode):
        gameStats = teamNode.getElementsByTagName("gameteam")[0]
        #TODO: throw exception if gameStats len != 1?
        return gameStats.attributes["R"].value


if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "tigsOnTop.settings"
    importer = ImportGamesCron()
    importer.importGames()
