from __future__ import unicode_literals

import datetime

from django.test import TestCase

from ..models import Game, GAME_STATUS_FINAL


class GameViewsetTest(TestCase):

    def _create_game(self):
        return Game.objects.create(
            themTeam='Yankees',
            usScore=1,
            themScore=0,
            startTime=datetime.datetime.now() - datetime.timedelta(hours=2),
            currentStatus=GAME_STATUS_FINAL)

    def test_get_latest_game(self):
        self._create_game()
        response = self.client.get('/api/v1/games/latest/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'currentStatus': u'FINAL',
            'themTeam': u'Yankees',
            'reaction': 'Shit yeah',
            'usScore': 1,
            'themScore': 0
        })

    def test_get_latest_game_none_found(self):
        response = self.client.get('/api/v1/games/latest/')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data, {
            'error': 'No games found',
        })
