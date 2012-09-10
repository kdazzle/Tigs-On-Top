from django.template import Context, loader, RequestContext, Template
from django.http import HttpResponse

def home(request):
    t = "gameTracker/home.html"
    c = None
    return loadPage(request, c, t)

def loadPage(request, context, template):
    t = loader.get_template(template)
    c = RequestContext(request, {})
    if context:
        c.update(context)
    return HttpResponse(t.render(c))
