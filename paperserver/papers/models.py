from django.db import models

import bibtexparser
from itertools import cycle

def rotate(lst): #Places the last element first
    return lst[-1:]+lst[:-1]


class Paper(models.Model):
    bibtex = models.TextField("Bibtex")
    link = models.URLField("Link")
    notes = models.TextField("Notes", blank=True)

    def __str__(self):
        return "[{}] {}, {}. {}, {}.".format(self.bibtexId(), self.authors(), self.title(), self.venue(), self.year())

    def parseBibtex(self):
        bibtexParsed = bibtexparser.loads(self.bibtex)
        return bibtexParsed.entries[0] if len(bibtexParsed.entries) > 0 else {}

    def getBibtexEntry(self, name):
        bibtexParsed = self.parseBibtex()
        return bibtexParsed[name] if name in bibtexParsed else ""

    def bibtexId(self):
        return self.getBibtexEntry("ID")

    def title(self):
        return self.getBibtexEntry("title")

    def year(self):
        return self.getBibtexEntry("year")

    def authors(self):
        cleanAuthorList = [] #Create an author list with no commas
        authorList = self.getBibtexEntry("author")
        if authorList:
            for author in authorList.split(" and "):
                authorSplit = [v.strip() for v in author.split(",")] # split on "," and trim whitespace
                authorSplit = rotate(authorSplit) #Put the first name first (if needed)
                cleanAuthorList.append(" ".join(authorSplit))
        return ", ".join(cleanAuthorList)

    def venue(self):
        bibtexParsed = self.parseBibtex()
        if "booktitle" in bibtexParsed:
            return bibtexParsed["booktitle"]
        elif "journal" in bibtexParsed:
            return bibtexParsed["journal"]
        elif "school" in bibtexParsed:
            return bibtexParsed["school"]
        else:
            return ""
