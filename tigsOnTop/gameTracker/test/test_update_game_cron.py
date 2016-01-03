from datetime import datetime

from mock import MagicMock, patch, ANY
from django.test import TestCase

from ..updateGameCron import UpdateGameCron
from ..models import Game, GAME_STATUS_IN_PROGRESS


class UpdateGameCronTest(TestCase):

    fixtures = [
        'Game.json'
    ]

    def test_update_game_called(self):
        """An active game was found and the _update method was called"""
        updater = UpdateGameCron()
        updater._updateGame = MagicMock(name='_updateGame')
        updater.updateGame()

        updater._updateGame.assert_called_once_with(ANY)


    @patch('gameTracker.importGames.urllib2')
    def test_update_in_progress(self, mock_urllib2):
        """Integration test to see that an in-progress game is updated"""
        xml = self._getGameUpdateXml()
        mock_urllib2.urlopen.return_value = xml
        updateCron = UpdateGameCron()
        updateCron.updateGame()

        active_game = Game.objects.get(currentStatus=GAME_STATUS_IN_PROGRESS)
        self.assertEqual(active_game.themTeam, "Mariners")
        self.assertEqual(active_game.usScore, 2)  # Score used to be 1

        mock_urllib2.urlopen.assert_called_once_with(ANY)

    def _getGameUpdateXml(self):
        return """
            <ig_game outs="0">
                  <game id="2014_06_28_detmlb_houmlb_1" league="AA" status="IN_PROGRESS"
                        start_time="4:10PM"
                        home_code=""/>
                  <team name="Mariners" code="">
                     <gameteam R="0" H="0" E="0"/>
                  </team>
                  <team name="Tigers" code="">
                     <gameteam R="2" H="0" E="0"/>
                  </team>
                  <inningnum inning="1" half="T"/>
                  <pitcher name="B. Oberholtzer"/>
                  <batter name="R. Davis"/>
               </ig_game>
            """.strip()


    @patch('gameTracker.importGames.urllib2')
    def test_update_flow(self, mock_urllib2):
        """Ensure methods are hit when updating a game"""
        xml = self._getGameUpdateXml()
        mock_urllib2.urlopen.return_value = xml
        updater = UpdateGameCron()
        updater._updateGameData = MagicMock(name="_updateGameData")
        updater.updateGame()

        updater._updateGameData.assert_called_once_with(ANY, ANY)

    def test_update_game_data(self):
        """A game is updated with the data from another game"""
        gameToUpdate = Game.objects.get(
            currentStatus=GAME_STATUS_IN_PROGRESS)
        assert gameToUpdate.usScore == 1, "The premise of the test is correct"

        updatedGame = self._getUpdatedGame()
        updateCron = UpdateGameCron()
        updateCron._updateGameData(gameToUpdate, updatedGame)

        game = Game.objects.get(pk=gameToUpdate.pk)
        self.assertEqual(game.usScore, 2)

    def _getUpdatedGame(self):
        return Game(
            mlbId="2014_06_28_detmlb_houmlb_1",
            currentStatus=GAME_STATUS_IN_PROGRESS,
            usScore=2,
            themScore=0,
            usTeam="Tigers",
            themTeam="Mariners",
            startTime=datetime.now(),
        )

    def test_updateGame(self):
        """The proper games are matched and updated"""
        gameToUpdate = Game.objects.get(
            currentStatus=GAME_STATUS_IN_PROGRESS)
        updater = UpdateGameCron()
        updater.getGamesFromMlbForDay = MagicMock(
            name='getGamesFromMlbForDay',
            return_value=[self._getUpdatedGame()])
        updater._updateGame(gameToUpdate)

        game = Game.objects.get(pk=gameToUpdate.pk)
        self.assertEqual(game.usScore, 2)
        updater.getGamesFromMlbForDay.assert_called_once_with(
            gameToUpdate.get_start_date())

    def test_getActiveGame(self):
        """A game that is in-progress is retrieved"""
        updater = UpdateGameCron()
        activeGame = updater._getActiveGame()

        self.assertIsNotNone(activeGame)
        self.assertEqual(activeGame.usScore, 1)
        self.assertEqual(activeGame.themTeam, "Mariners")
