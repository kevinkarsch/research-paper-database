from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader

from .models import Paper


def index(request):
    paperDatabase = Paper.objects.order_by('-id')
    paperList = []
    for paper in paperDatabase:
        paperList.append({
            'id' : paper.id,
            'bibtexId' : paper.bibtexId(),
            'title' : paper.title(),
            'authors' : paper.authors(),
            'venue' : paper.venue(),
            'year' : paper.year(),
            'link' : paper.link,
        })

    context = {'paperList': paperList}
    return render(request, 'papers/index.html', context)


def paperInfo(request, paper_id):
    paper = get_object_or_404(Paper, pk=paper_id)

    context = {
        'id' : paper.id,
        'bibtexId' : paper.bibtexId(),
        'title' : paper.title(),
        'authors' : paper.authors(),
        'venue' : paper.venue(),
        'year' : paper.year(),
        'link' : paper.link,
        'bibtex' : paper.bibtex,
        'notes' : paper.notes if paper.notes else "(none)",
    }

    return render(request, 'papers/paperInfo.html', context)


def downloadBibtex(request):
    paperDatabase = Paper.objects.order_by('-id')
    bibtexEntries = []
    for paper in paperDatabase:
        bibtexEntries.append(paper.bibtex)

    response = HttpResponse(content_type='application/x-bibtex')
    response['Content-Disposition'] = 'attachment; filename="papers.bibtex"'
    response.write("\n\n".join(bibtexEntries))

    return response
