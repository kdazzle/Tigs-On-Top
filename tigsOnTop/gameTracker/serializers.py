from __future__ import unicode_literals

from rest_framework import serializers

from .models import Game
from .views import get_winning_dialog


class GameSerializer(serializers.ModelSerializer):

    reaction = serializers.SerializerMethodField()

    def get_reaction(self, game):
        return get_winning_dialog(game)

    class Meta:
        model = Game
        fields = ('themTeam', 'usScore', 'themScore', 'currentStatus', 'reaction')
