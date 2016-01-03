from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .views import getActiveGame
from .serializers import GameSerializer
from .models import Game


class GameViewSet(viewsets.ViewSet):

    queryset = Game.objects.all()

    @list_route(['GET'])
    def latest(self, request, pk=None):
        game = getActiveGame()
        if game:
            serializer = GameSerializer(game)
            return Response(serializer.data)
        else:
            return Response({'error': 'No games found'}, status=500)
