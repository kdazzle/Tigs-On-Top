import datetime
from logging import getLogger

import pytz
from django.utils.timezone import utc
from django.template import Context, loader, RequestContext, Template
from django.http import HttpResponse
from django.conf import settings

from .models import (
    Game, GAME_STATUS_DELAYED, GAME_STATUS_IN_PROGRESS, GAME_STATUS_FINAL)


l = getLogger(__name__)
THE_TEAM = settings.THE_TEAM
TIMEZONE = pytz.timezone(settings.TIME_ZONE)


def home(request):
    try:
        game = getActiveGame()
        winningDialog = getWinningDialog(game)
    except Exception as e:
        l.exception(e)
        game = None
        winningDialog = "Uh oh, there was an error and I have no idea right now."

    t = "gameTracker/home.html"
    c = RequestContext(request, {
        "game": game,
        "winningDialog": winningDialog,
    })
    return loadPage(request, c, t)


def getActiveGame():
    """
    :return {Game|None}: the game that is currently in progress, the most
    recently finished game, or None
    """
    utcNow = datetime.datetime.utcnow().replace(tzinfo=utc)
    active_statuses = (
        settings.GAME_STATUS_IN_PROGRESS,
        settings.GAME_STATUS_FINAL,
        settings.GAME_STATUS_DELAYED)

    games = Game.objects.filter(
        startTime__lte=utcNow,
        currentStatus__in=active_statuses).order_by("-startTime")

    if games:
        return games[0]
    else:
        return None


def getWinningDialog(game):
    """
    Get a pleasantly upbeat message (to be shown to the user) about the
     performance of the Tigers.

    :param {Game|None} game:
    :return: {string}
    """
    if not game:
        return "Well, no. But we got it next season!"

    isFinished = game.is_finished()
    if game.usScore > game.themScore and isFinished is True:
        return "Shit yeah"
    elif game.usScore > game.themScore and isFinished is False:
        return "No, but we're winning"
    elif game.usScore < game.themScore and isFinished is False:
        return "No. But we still got a chance."
    elif game.usScore == game.themScore and isFinished is False:
        return "Naw, it's tied"
    elif game.usScore == game.themScore and isFinished is True:
        return "Almost. It was tied."
    else:
        return "Not this time, gents"


def loadPage(request, context, template):
    t = loader.get_template(template)
    c = RequestContext(request, {})
    if context:
        c.update(context)
    return HttpResponse(t.render(c))
