import cherrypy
import json

import scholar
import torScholar
import dataCollector

import os
import os.path



current_dir = os.path.dirname(os.path.abspath(__file__))



class root_page(object):
    _cp_config = \
    {
        "tools.staticdir.on"    : True,
        "tools.staticdir.dir"   : os.path.join(current_dir, "..", "www"),
        "tools.staticdir.index" : "index.html",
    }

    @cherrypy.expose
    def getPaper(self, *args, **kwargs):

        paperTitle = kwargs["title"];

        cherrypy.response.headers["Content-Type"] = "application/json"

        if paperTitle:

            querier   = torScholar.TorScholarQuerier()
            paperDict = dataCollector.getPaper(paperTitle, querier)

            message =                           \
            {                                   \
                "title"   : paperDict["title"], \
                "authors" : "Z. DeVito, N. Joubert, F. Palacios, S. Oakley, M. Medina, M. Barrientos, E. Elsen, F. Ham, A. Aiken, K. Duraisamy, E. Darve, J. Alonso, P. Hanrahan", \
                "venue"   : "SC",
                "year"    : paperDict["year"]
            }

            return json.dumps(message);
        else:
            raise cherrypy.HTTPError(500, "You need to supply a paper title")

    @cherrypy.expose
    def getAllCitingPapers(self, *args, **kwargs):

        message = {"papers": [{"title" : "haha", "authors":"zach", "venue": "siggraph", "year": "2011" }]}
        return json.dumps(message);



cherrypy.quickstart(root_page())
