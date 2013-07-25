import cherrypy
import json

import scholar
import torScholar

import os.path

current_dir = os.path.dirname(os.path.abspath(__file__))

class root_page(object):
    _cp_config = {'tools.staticdir.on' : True,
                  'tools.staticdir.dir' : os.path.join(current_dir, '..', 'www'),
                  'tools.staticdir.index' : 'index.html',
    }

    @cherrypy.expose
    def index(self, *args, **kwargs):
        papertitle = kwargs['paper_name']

        querier = torScholar.TorScholarQuerier()
        papersDict = dataCollector.getAllPapers(papertitle, querier)

        papersSorted = sorted(papersDict.iteritems(), key=lambda x: x[1][0]['num_citations'], reverse=True)

        html = "<html><head></head><body>"
        html = html + "<h1>Citation Search Results</h1>"
        html = html + "<h3>" + str(len(papersSorted)) + " papers cited (directly or indirectly) \"" + papertitle + "\"</h3>"
        html = html + "<table>"
        for t,pair in papersSorted:
            a, depth = pair
            year = str(a['year']) if a['year'] else "-"
            url_citations = a['url_citations'] if a['url_citations'] else "#"
            num_citations = str(a['num_citations']) if a['num_citations'] else "0"
            url = a['url'] if a['url'] else "#"
            html = html + "<tr><td><a href='" + url_citations + "'> "+ num_citations + " Citations</a></td><td>" + str(depth) + " Deep</td><td>" + year + "</td><td><a href='"+ url +"'>" + t + "</a></td></tr>"
        html = html + "</table></body></html>"
        return html
    
    @cherrypy.expose
    def checkPaper(self, *args, **kwargs):

        papertitle = kwargs['title'];

        cherrypy.response.headers['Content-Type'] = "application/json"
        if papertitle:
            message = {"title" :"Liszt: a domain specific language for building portable mesh-based PDE solvers", "authors":  "Z. DeVito, N. Joubert, F. Palacios, S. Oakley, M. Medina, M. Barrientos, E. Elsen, F. Ham, A. Aiken, K. Duraisamy, E. Darve, J. Alonso, P. Hanrahan", "venue": "SC", "year": "2011" } 
            return json.dumps(message);
        else:
            raise cherrypy.HTTPError(500, "You need to supply a paper title")

    @cherrypy.expose
    def getCitationGraph(self, *args, **kwargs):
        message = {"papers": [{"title" : "haha", "authors":"zach", "venue": "siggraph", "year": "2011" }]}
        return json.dumps(message);

cherrypy.quickstart(root_page())