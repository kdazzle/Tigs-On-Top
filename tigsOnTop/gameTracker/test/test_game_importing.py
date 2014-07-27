from mock import MagicMock, patch, ANY
from django.test import TestCase


from ..importGames import ImportGamesCron
from ..models import Game, GAME_STATUS_IN_PROGRESS


class ImportGameTest(TestCase):

    fixtures = [
        'Game.json'
    ]

    @patch('gameTracker.importGames.urllib2')
    def test_getGamesFromMlbForDay(self, mock_urllib2):
        """We can convert data returned from the MLB API into Games just fine"""
        xml = """
            <scoreboard>
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
           </scoreboard>
            """.strip()
        mock_urllib2.urlopen.return_value = xml

        game = Game.objects.get(currentStatus=GAME_STATUS_IN_PROGRESS)
        importer = ImportGamesCron()
        games = importer.getGamesFromMlbForDay(game.get_start_date())

        self.assertEqual(len(games), 1)
        self.assertEqual(games[0].usScore, 2)
