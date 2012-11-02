from django.shortcuts import render_to_response, get_object_or_404
from wpe.sna.models import Messages, Pairs
from django.http import Http404
from django.template import RequestContext, Context
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q

import re
from string import punctuation
from operator import itemgetter

# Create your views here.
def home(request):
    #Create List of all messages
    allmsgs = list(Messages.objects.all())

    #Number of Messages in each cmc
    fp = Messages.objects.filter(cmc='fp')
    fc = Messages.objects.filter(cmc='fc')
    jp = Messages.objects.filter(cmc='jp')
    jc = Messages.objects.filter(cmc='jc')
    n = Messages.objects.filter(cmc='n')

    # Number of Users posting messages to each of the CMC
    fpu = fp.values('author').distinct()
    fcu = fc.values('author').distinct()
    jpu = jp.values('author').distinct()
    jcu = jc.values('author').distinct()
    nu = n.values('author').distinct()


    #Pairs
    fEdge = Pairs.objects.filter(CMC='f')
    jEdge = Pairs.objects.filter(CMC='j')
    nEdge = Pairs.objects.filter(CMC='n')

    #unique pairs
    fUEdge = fEdge.values('sender').distinct()
    jUEdge = jEdge.values('sender').distinct()
    nUEdge = nEdge.values('sender').distinct()

    return render_to_response('index.html',
                          { 'fp': fp, 'fc': fc, 'jp': jp, 'jc': jc, 'nm': n,
                          'allmsgs':allmsgs, 'fpNodes':fpu, 'fcNodes':fcu,
                          'jpNodes':jpu, 'jcNodes':jcu, 'nNodes':nu,
                          'fNodes': fp.count() + fc.count(), 'jNodes': jp.count() + jc.count(),
                          'fEdge': fEdge, 'jEdge': jEdge, 'nEdge': nEdge,
                          'fUEdge': fUEdge, 'jUEdge': jUEdge, 'nUEdge': nUEdge,
                          },
                          context_instance=RequestContext(request))