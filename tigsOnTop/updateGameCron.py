#!/usr/local/bin/python2.7
import os
import pytz

from tigsOnTop import settings
from importGames import ImportGamesCron
from gameTracker.models import Game


class UpdateGameCron(ImportGamesCron):
    TIMEZONE = pytz.timezone(settings.TIME_ZONE)

    def updateGame(self):
        """
        If there is a game that is currently being played, get updates from
        the MLB API.
        """
        activeGame = self._getActiveGame()
        if activeGame is not None:
            self._updateGame(activeGame)

    def _getActiveGame(self):
        """
        If a game is being played right now, return it. Otherwise, return None.

        :return: {Game|None}
        """
        active_statuses = (
            settings.GAME_STATUS_IN_PROGRESS,
            settings.GAME_STATUS_DELAYED,
        )
        activeGames = Game.objects.filter(currentStatus__in=active_statuses)

        if len(activeGames) > 0:
            return activeGames[0]
        else:
            return None

    def _updateGame(self, game):
        """
        Gets updates from the MLB API about the given game.

        :param {Game} game
        """
        games_on_gameday = self.getGamesToImportByDay(game.get_start_date())
        for game in games_on_gameday:
            try:
                matchingGame = Game.objects.get(startTime=game.startTime)
                self._updateGame(matchingGame, game)
            except Game.DoesNotExist:
                continue

    def _updateGame(self, matchingGame, updatedGame):
        """
        Update an existing game with new data.

        :param matchingGame: the already existing game
        :param updatedGame: the updated game taken from the xml data
        """
        matchingGame.usScore = updatedGame.usScore
        matchingGame.themScore = updatedGame.themScore
        matchingGame.currentStatus = updatedGame.currentStatus
        matchingGame.save()


if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "tigsOnTop.settings"
    updater = UpdateGameCron()
    updater.updateGame()
