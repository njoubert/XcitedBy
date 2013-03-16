
import scholar

def getAllPapers(papertitle):
    papers = scholar.papers_by_title(papertitle)

    print "Found paper:"
    print "  ", papers[0]['title'], papers[0]['papernumber']
    print "  ", "with", papers[0]['num_citations'], "citations"

    # allStuff = scholar.citations_by_papernr(papernr);
    # print "I downloaded", len(allStuff), "papers"
    # for al in allStuff:
    #   print al.as_txt();

    allPapers = dict()

    toCheckPapers = [papers[0]];
    while (len(toCheckPapers) > 0):
        paper = toCheckPapers.pop(0)
        if (paper['title'] in allPapers):
            continue
        allPapers[paper['title']] = paper;

        if (paper['papernumber']):
            newCitations = scholar.citations_by_papernr(paper['papernumber'])
            for art in newCitations:
                if (not (art['title'] in allPapers)):
                    toCheckPapers.append(art)

    return allPapers


def main():

    papertitle = "Liszt: a domain specific language for building portable mesh-based PDE solvers"
    papernr = "11546469924168842438"
    
    print "Found citations for first paper:", len(allPapers)
    for key in allPapers:
    	print key


if __name__ == "__main__":
    main()
