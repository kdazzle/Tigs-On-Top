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
    try:
        game = getActiveGame()
        isFinal = isFinalScore(game)
        winningDialog = getWinningDialog(game, isFinal)
    except Exception:
        game = None
        winningDialog = "Uh oh, there was an error and I have no idea right now."

    t = "gameTracker/home.html"
    c = RequestContext(request, {
         "game": game,
         "winningDialog": winningDialog,
         })
    return loadPage(request, c, t)

def getActiveGame():
    utcNow = datetime.datetime.utcnow().replace(tzinfo=utc)
    games = Game.objects.filter(startTime__lte=utcNow).order_by("-startTime")
    if games:
        return games[0]
    else:
        return None

def isFinalScore(game):
    if game and game.currentStatus == "FINAL":
        return True
    else:
        return False

def getWinningDialog(game, isFinal):
    if not game:
        return "Well, no. But we got it next season!"
    elif game.usScore > game.themScore and isFinal is True:
        return "Shit yeah"
    elif game.usScore > game.themScore and isFinal is False:
        return "No, but we're winning"
    elif game.usScore < game.themScore and isFinal is False:
        return "No. But we still got a chance."
    elif game.usScore == game.themScore and isFinal is False:
        return "Naw, it's tied"
    elif game.usScore == game.themScore and isFinal is True:
        return "Almost. It was tied."
    else:
        return "Not this time, gents"

def loadPage(request, context, template):
    t = loader.get_template(template)
    c = RequestContext(request, {})
    if context:
        c.update(context)
    return HttpResponse(t.render(c))
