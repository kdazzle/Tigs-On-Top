#!/usr/local/bin/python2.7
import os
import pytz
from logging import getLogger

from tigsOnTop import settings
from .importGames import ImportGamesCron
from .models import Game, GAME_STATUS_IN_PROGRESS, GAME_STATUS_DELAYED


l = getLogger(__name__)


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
        Get the most recent active game or return None

        :return: {Game|None}
        """
        active_statuses = (
            GAME_STATUS_IN_PROGRESS,
            GAME_STATUS_DELAYED,
        )
        activeGames = Game.objects.filter(
            currentStatus__in=active_statuses).order_by("-startTime")

        if len(activeGames) > 0:
            game = activeGames[0]
            l.info("Active game fetched: {}".format(game))
            return game
        else:
            l.info("No active games")
            return None

    def _updateGame(self, game):
        """
        Gets updates from the MLB API about the given game.

        :param {Game} game  an in-progress game
        """
        games_from_mlb = self.getGamesFromMlbForDay(game.get_start_date())
        for updatedGame in games_from_mlb:
            try:
                matchingGame = Game.objects.get(mlbId=updatedGame.mlbId)
                self._updateGameData(matchingGame, updatedGame)
            except Game.DoesNotExist:
                l.debug("No matching game found for {}".format(updatedGame))

    def _updateGameData(self, gameToUpdate, updatedGame):
        """
        Update an existing game with new data.

        :param gameToUpdate: the already existing game
        :param updatedGame: the updated game taken from the xml data
        """
        gameToUpdate.usScore = updatedGame.usScore
        gameToUpdate.themScore = updatedGame.themScore
        gameToUpdate.currentStatus = updatedGame.currentStatus
        gameToUpdate.save()
        l.info("Updated game: {}".format(gameToUpdate))


if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "tigsOnTop.settings"
    updater = UpdateGameCron()
    updater.updateGame()
