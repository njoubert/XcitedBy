
import scholar



def main():

    papertitle = "Liszt: a domain specific language for building portable mesh-based PDE solvers"
    papernr = "11546469924168842438"


    papers = scholar.papers_by_title(papertitle)

    print "Found paper:"
    print "  ", papers[0]['title'], papers[0]['papernumber']
    print "  ", "with", papers[0]['num_citations'], "citations"

    # allStuff = scholar.citations_by_papernr(papernr);
    # print "I downloaded", len(allStuff), "papers"
    # for al in allStuff:
    # 	print al.as_txt();


    allCitations = [];
    toCheckCitations = [papers[0]];
    while (len(toCheckCitations) > 0):
    	paper = toCheckCitations.pop(0)
    	if (not paper['papernumber']):
    		print 'Missing a papernumber on', paper['title']
    		continue
    	newCitations = scholar.citations_by_papernr(paper['papernumber'])
    	for art in newCitations:
    		already = False
    		for knownArt in allCitations:
    			if (art['papernumber'] is knownArt['papernumber']):
    				already = True
    		if (not already):
    			allCitations.append(art)
    			#toCheckCitations.append(art)




    
    print "Found citations for first paper:", len(allCitations)
    for c in allCitations:
    	print c.as_txt();


if __name__ == "__main__":
    main()
