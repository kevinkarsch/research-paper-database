from django.db import models

import bibtexparser
from itertools import cycle

def rotate(lst): #Places the last element first
    return lst[-1:]+lst[:-1]

def extractAuthors(bibtexEntry):
    cleanAuthorList = [] #Create an author list as "First1 Last1, First2 Last2, etc"
    authorList = bibtexEntry.get("author")
    if authorList:
        for author in authorList.split(" and "):
            authorSplit = [v.strip() for v in author.split(",")] # split on "," and trim whitespace
            authorSplit = rotate(authorSplit) #Put the first name first (if needed)
            cleanAuthorList.append(" ".join(authorSplit))
    return ", ".join(cleanAuthorList)

def extractVenue(bibtexEntry):
    if "booktitle" in bibtexEntry:
        return bibtexEntry["booktitle"]
    elif "journal" in bibtexEntry:
        return bibtexEntry["journal"]
    elif "school" in bibtexEntry:
        return bibtexEntry["school"]
    else:
        return ""


class Paper(models.Model):
    bibtex = models.TextField("Bibtex")
    link = models.URLField("Link", blank=True)
    notes = models.TextField("Notes", blank=True)

    def __str__(self):
        bib = self.asDict()
        return "[{}] {}, {}. {}, {}.".format(bib["bibtexId"], bib["authors"], bib["title"], bib["venue"], bib["year"])

    def asDict(self):
        bibtexParsed = bibtexparser.loads(self.bibtex)
        bibtexEntry = bibtexParsed.entries[0] if len(bibtexParsed.entries) > 0 else {}
        return {
            "id": self.id,
            "bibtex": self.bibtex,
            "link": self.link,
            "notes": self.notes if self.notes else "(None)",
            "bibtexId": bibtexEntry["ID"] if "ID" in bibtexEntry else "",
            "title": bibtexEntry["title"] if "title" in bibtexEntry else "",
            "year": bibtexEntry["year"] if "year" in bibtexEntry else "",
            "authors": extractAuthors(bibtexEntry),
            "venue": extractVenue(bibtexEntry),
        }
