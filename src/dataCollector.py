
import scholar

def getPaper(papertitle, querier=scholar.ScholarQuerier()):

    papers = scholar.papers_by_title(papertitle, querier)

    print "[DATA COLLECTOR INFO] Found paper:"
    print "  ", papers[0]["title"], "(", papers[0]["papernumber"], ")"
    print "  ", "with", papers[0]["num_citations"], "citations"
    print

    return papers[0]

def getAllCitingPapers(papertitle, querier=scholar.ScholarQuerier()):

    paper         = getPaper(papertitle, querier)
    allPapers     = dict()
    toCheckPapers = [(paper,0)]

    while (len(toCheckPapers) > 0):

        paper, depth = toCheckPapers.pop(0)

        if (paper["title"] in allPapers):
            continue

        allPapers[paper["title"]] = (paper, depth)

        if (paper["papernumber"]):

            print "[DATA COLLECTOR INFO] " + paper["title"]

            newCitations = scholar.citations_by_papernr(paper["papernumber"], querier)

            for art in newCitations:
                if (not (art["title"] in allPapers)):
                    toCheckPapers.append((art,depth+1))

    return allPapers
