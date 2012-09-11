import urllib2
from xml.dom import minidom
import datetime

from django.template import Context, loader, RequestContext, Template
from django.http import HttpResponse
from django.conf import settings

THE_TEAM = settings.THE_TEAM

def home(request):
    areWeWinning = isWeWinning(gameData["score"])
    isFinal = isFinalScore(tigersGame)

    t = "gameTracker/home.html"
    c = RequestContext(request, {
         'remoteData': tigersGame.toxml(),
         "scores": gameData["score"],
         "winningDialog": getWinningDialog(areWeWinning, isFinal),
         "url": gameDataUrl,
         })
    return loadPage(request, c, t)

def isWeWinning(scores):    
    for team, score in scores.iteritems():
        if team == THE_TEAM:
            ourScore = score
        else:
            theirScore = score

    return ourScore > theirScore

def isFinalScore(tigersGameNode):
    gameDataNode = tigersGameNode.getElementsByTagName("game")[0]
    status = gameDataNode.attributes["status"].value
    if status == "FINAL":
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
