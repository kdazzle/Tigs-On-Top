import urllib2
from xml.dom import minidom
import datetime
import pytz

from django.utils.timezone import utc
from django.template import Context, loader, RequestContext, Template
from django.http import HttpResponse
from django.conf import settings
from gameTracker.models import Game

THE_TEAM = settings.THE_TEAM
TIMEZONE = pytz.timezone(settings.TIME_ZONE)

def home(request):
    game = getActiveGame()
    areWeWinning = isWeWinning(game)
    isFinal = isFinalScore(game)

    t = "gameTracker/home.html"
    c = RequestContext(request, {
         "game": game,
         "winningDialog": getWinningDialog(areWeWinning, isFinal),
         })
    return loadPage(request, c, t)

def getActiveGame():
    utcNow = datetime.datetime.utcnow().replace(tzinfo=utc)
    print utcNow
    games = Game.objects.filter(startTime__lte=utcNow).order_by("-startTime")
    print "Game length: %s" % len(games)    
    print games[0]
    return games[0]

def isWeWinning(game):   
    return game.usScore > game.themScore

def isFinalScore(game):
    if game.currentStatus == "FINAL":
        return True
    else:
        return False

def getWinningDialog(areWeWinning, isFinal):
    if areWeWinning is True and isFinal is True:
        return "Shit yeah"
    elif areWeWinning is True and isFinal is False:
        return "No, but we're winning"
    elif areWeWinning is False and isFinal is False:
        return "No, and we're not quite winning"
    else:
        return "Not this time, gents"

def loadPage(request, context, template):
    t = loader.get_template(template)
    c = RequestContext(request, {})
    if context:
        c.update(context)
    return HttpResponse(t.render(c))
