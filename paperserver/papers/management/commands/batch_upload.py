from django.core.management.base import BaseCommand, CommandError
from papers.models import Paper

import bibtexparser
import os
import sys


class Command(BaseCommand):
    help = "Upload multiple bibtex files at once"

    def add_arguments(self, parser):
        parser.add_argument("bibtex_file")

    def handle(self, *args, **options):
        inBibtexFile = options["bibtex_file"]

        if not os.path.isfile(inBibtexFile):
            self.stdout.write(self.style.ERROR("File '{}' does not exist.".format(inBibtexFile)))
            sys.exit()

        try:
            with open(inBibtexFile, encoding="utf-8") as bibtexFile:
                bibtexData = bibtexparser.load(bibtexFile)
        except:
            self.stdout.write(self.style.WARNING("Failed reading file with UTF-8 encoding, atttempting to read as Latin-1."))
            try:
                with open(inBibtexFile, encoding="ISO-8859-1") as bibtexFile:
                    bibtexData = bibtexparser.load(bibtexFile)
            except:
                self.stdout.write(self.style.ERROR("Failed reading file with either UTF-8 or Latin-1 encoding."))
                sys.exit()

        bibWriter = bibtexparser.bwriter.BibTexWriter()
        bibWriter.contents = ["entries"]
        bibWriter.indent = "    "
        for entry in bibtexData.entries:
            singleEntryBibDatabase = bibtexparser.bibdatabase.BibDatabase
            singleEntryBibDatabase.entries = [entry]
            bibtex = bibtexparser.dumps(singleEntryBibDatabase, bibWriter)
            link = None
            for linkKey in ["url", "URL", "doi", "DOI"]:
                if linkKey in entry:
                    link = entry[linkKey]
                    break
            if not link:
                link = 'https://www.google.com/search?q="{}"'.format(entry["title"])

            paper = Paper(bibtex=bibtex, link=link)
            paper.save()
            self.stdout.write(self.style.SUCCESS("  -- Imported: {}".format(paper)))

        self.stdout.write(self.style.SUCCESS("Successfully imported {} papers.".format(len(bibtexData.entries))))
