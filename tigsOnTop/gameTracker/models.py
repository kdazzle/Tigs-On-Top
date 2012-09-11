from django.db import models
from tigsOnTop import settings

class Game(models.Model):
    usTeam = models.CharField(max_length=64, default=settings.THE_TEAM)
    themTeam = models.CharField(max_length=64)
    usScore = models.IntegerField(default=0)
    themScore = models.IntegerField(default=0)
    startTime = models.DateTimeField()
    addDate = models.DateTimeField(auto_now_add=True)

    def save(self):
        """Saves game if there is not already a game set for the same datetime"""
        matchingGames = Game.objects.filter(startTime=self.startTime)    
        if len(matchingGames) == 0:
            super(Game, self).save()
