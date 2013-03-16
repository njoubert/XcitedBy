
import scholar



def main():

    papertitle = "Liszt: a domain specific language for building portable mesh-based PDE solvers"
    papernr = "11546469924168842438"


    papers = scholar.papers_by_title(papertitle)

    print "Found paper:"
    print "  ", papers[0]['title'], papers[0]['papernumber']
    print "  ", "with", papers[0]['num_citations'], "citations"


    paperNumber = papers[0]['papernumber']

    while (True):
    	newCitations = scholar.citations_by_papernr(paperNumber)


    
    print "Found citations for first paper:", len(citations)


if __name__ == "__main__":
    main()
