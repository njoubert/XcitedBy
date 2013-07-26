import cherrypy
import json

import scholar
import torScholar
import dataCollector

import os
import os.path
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))



class API(object):

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

class Root():
    _cp_config = \
    {
        "tools.staticdir.on"    : True,
        "tools.staticdir.dir"   : os.path.join(current_dir, "..", "www"),
        "tools.staticdir.index" : "index.html",
    }

root = Root()
root.data = API();

class RedirectExceptions(cherrypy.process.plugins.SimplePlugin):

    def start(self):
        self.stderr_file = open("stderr.log", "w");
        self.stdout_file = open("stdout.log", "w");
        self.original_stderr = sys.stderr
        self.original_stdout = sys.stdout
        
        sys.stderr = self.stderr_file;
        sys.stdout = self.stdout_file;

    def stop(self):
        sys.std_err = self.original_stderr;
        sys.stdout = self.original_stdout;
        self.stdout_file.close();
        self.stderr_file.close()


for arg in sys.argv:
    if arg == "PROD":
        cherrypy.config.update({'environment': 'production',
                                'log.error_file': 'site.log',
                                'server.socket_port': 61337});
        cherrypy.engine.redirectexceptions = RedirectExceptions(cherrypy.engine);
        cherrypy.engine.redirectexceptions.subscribe();

cherrypy.quickstart(root)
