
import scholar

def getPaper(papertitle, querier=scholar.ScholarQuerier()):

    papers = scholar.papers_by_title(papertitle, querier)

    if len(papers) > 0:
        print "[DATA COLLECTOR INFO]"
        print "  Found paper:"
        print "    ", papers[0]["title"], "(", papers[0]["papernumber"], ")"
        print "    ", "with", papers[0]["num_citations"], "citations"
        print

        return papers[0]
    else:
        print "[DATA COLLECTOR INFO]"
        print "  Didn't find any papers."
        print

        return None

def getAllCitingPapersIncremental(papertitle, querier=scholar.ScholarQuerier()):

    paper                                 = getPaper(papertitle, querier)
    numPapersProcessedCumulative          = 1
    numDuplicatesRemoved                  = 0
    paper["depth"]                        = 0
    paper["numPapersProcessedCumulative"] = numPapersProcessedCumulative
    paper["numDuplicatesRemoved"]         = numDuplicatesRemoved
    allPapers                             = dict()
    toCheckPapers                         = [paper]

    while (len(toCheckPapers) > 0):

        paper = toCheckPapers.pop(0)

        if paper["title"] in allPapers:

            numDuplicatesRemoved = numDuplicatesRemoved + 1

        else:

            print "[DATA COLLECTOR INFO] Found paper: " + paper["title"]

            paper["numPapersProcessedCumulative"] = numPapersProcessedCumulative
            paper["numDuplicatesRemoved"]         = numDuplicatesRemoved
            allPapers[paper["title"]]             = paper

            yield paper

            if (paper["papernumber"]):

                newCitations                 = scholar.citations_by_papernr(paper["papernumber"], querier)
                numPapersProcessedCumulative = numPapersProcessedCumulative + len(newCitations)

                for art in newCitations:
                    
                    art["depth"] = paper["depth"] + 1
                    toCheckPapers.append(art)
