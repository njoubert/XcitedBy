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

    #
    # Get papers using TOR proxying (assumes TOR is running and is correctly configured)
    #
    # querier = torScholar.TorScholarQuerier()
    # papersDict = dataCollector.getAllPapers(papertitle, querier)
    #

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