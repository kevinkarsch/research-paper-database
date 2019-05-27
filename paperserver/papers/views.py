from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader

from .models import Paper


def index(request):
    paperDatabase = Paper.objects.order_by('-id')
    paperList = [paper.asDict() for paper in paperDatabase]
    context = {'paperList': paperList}
    return render(request, 'papers/index.html', context)


def paperInfo(request, paper_id):
    paper = get_object_or_404(Paper, pk=paper_id)
    return render(request, 'papers/paperInfo.html', paper.asDict())


def downloadBibtex(request):
    paperDatabase = Paper.objects.order_by('-id')
    bibtexEntries = [paper.bibtex for paper in paperDatabase]

    response = HttpResponse(content_type='application/x-bibtex')
    response['Content-Disposition'] = 'attachment; filename="papers.bibtex"'
    response.write("\n\n".join(bibtexEntries))

    return response
