
import scholar

def getAllPapers(papertitle, querier=scholar.ScholarQuerier()):

    papers = scholar.papers_by_title(papertitle, querier)

    print "Found paper:"
    print "  ", papers[0]["title"], "(", papers[0]["papernumber"], ")"
    print "  ", "with", papers[0]["num_citations"], "citations"
    print

    allPapers = dict()

    toCheckPapers = [(papers[0],0)]

    while (len(toCheckPapers) > 0):

        paper, depth = toCheckPapers.pop(0)

        if (paper["title"] in allPapers):
            continue

        allPapers[paper["title"]] = (paper, depth)

        if (paper["papernumber"]):

            print paper["title"]

            newCitations = scholar.citations_by_papernr(paper["papernumber"], querier)

            for art in newCitations:
                if (not (art["title"] in allPapers)):
                    toCheckPapers.append((art,depth+1))

    return allPapers
