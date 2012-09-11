import urllib2
from xml.dom import minidom
from datetime import datetime as DateTime
import datetime
import pytz
import sys

from tigsOnTop import settings
from gameTracker.models import Game

class ImportGamesCron():
    TIMEZONE = pytz.timezone(settings.TIME_ZONE)
    IMPORT_ADVANCE_DAYS = settings.IMPORT_ADVANCE_DAYS

    def importGames(self):
        dateRange = self.getDateRange()
        for day in dateRange:
            self.importGame(day)

    def getDateRange(self):
        base = self.TIMEZONE.localize(datetime.datetime.today())
        dateList = [ 
                base + datetime.timedelta(days=x) for x in range(-1,self.IMPORT_ADVANCE_DAYS) 
            ]
        return dateList

    def importGame(self, day):
        gameDataUrl = self.getGameDataUrl(day)
        remoteDataXml = minidom.parse(urllib2.urlopen(gameDataUrl))
        teamList = remoteDataXml.getElementsByTagName('team')
        tigersGames = self.getGamesFromTeamList(teamList)
        self.saveGames(tigersGames, day)

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

    def saveGames(self, games, day):
        for game in games:
            newGame = self.getGameData(game, day)
            newGame.save()
        
    def getGameData(self, gameNode, day):
        teamsXml = gameNode.getElementsByTagName("team")
        teamsData = {}
        game = Game()
        startTime = self.getStartTime(gameNode, day)
        game.startTime = startTime
        for team in teamsXml:
            currentTeamName = team.attributes["name"].value
            teamsData[currentTeamName] = team
            if currentTeamName == settings.THE_TEAM:
                game.usTeam = settings.THE_TEAM
            else:
                game.themTeam = currentTeamName
        
        return game

        #score = self.getGameScore(teamsData)
        #teamsData["score"] = score
        #return teamsData
        
    def getStartTime(self, gameNode, day):
        gameDataNode = gameNode.getElementsByTagName("game")[0]
        startTime = gameDataNode.attributes["start_time"].value
        startDay = "%s %s %s" % (day.month, day.day, day.year)
        return DateTime.strptime("%s %s" % (startDay, startTime), "%m %d %Y %I:%M%p")

    def getGameScore(self, teamsData):
        scores = {}    
        for team, data in teamsData.iteritems():
            scores[team] = self.getScoreFromTeamNode(data)
        return scores

    def getScoreFromTeamNode(self, teamNode):
        gameStats = teamNode.getElementsByTagName("gameteam")[0]
        #TODO: throw exception if gameStats len != 1
        return gameStats.attributes["R"].value


if __name__ == "__main__":
    importer = ImportGamesCron()
    importer.importGames()
