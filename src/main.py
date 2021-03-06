import cherrypy
import json

import scholar
import torScholar
import dataCollector
import torUtils

import os
import os.path
import sys
import time
import argparse

class API(object):

    def __init__(self, commandLineArgs):
        self.commandLineArgs = commandLineArgs

    def packetize(self, string):
        return ("%s***SEP***" % string)

    @cherrypy.expose
    def getPaper(self, *args, **kwargs):

        paperTitle = kwargs["title"];
        cherrypy.response.headers["Content-Type"] = "application/json"

        if paperTitle:

            querier = torScholar.TorScholarQuerier(self.commandLineArgs)
            paper   = dataCollector.getPaper(paperTitle, querier)

            if paper is not None:
                message =                           \
                {                                   \
                    "title"   : paper["title"], \
                    "authors" : "Z. DeVito, N. Joubert, F. Palacios, S. Oakley, M. Medina, M. Barrientos, E. Elsen, F. Ham, A. Aiken, K. Duraisamy, E. Darve, J. Alonso, P. Hanrahan", \
                    "venue"   : "SC",
                    "year"    : paper["year"]
                }
                return json.dumps(message)
            else:
                return json.dumps(None)

        else:

            raise cherrypy.HTTPError(500, "You need to supply a paper title")

    @cherrypy.expose
    def getAllCitingPapers(self, *args, **kwargs):

        paperTitle                                = kwargs["title"];
        cherrypy.response.headers["Content-Type"] = "application/json"
        querier                                   = torScholar.TorScholarQuerier(self.commandLineArgs)
        papers                                    = dataCollector.getAllCitingPapers(paperTitle)
        paperMessages                             = []

        for paper in papers:

            paperMessage =                      \
            {                                   \
                "title"   : paperDict["title"], \
                "authors" : "Z. DeVito, N. Joubert, F. Palacios, S. Oakley, M. Medina, M. Barrientos, E. Elsen, F. Ham, A. Aiken, K. Duraisamy, E. Darve, J. Alonso, P. Hanrahan", \
                "venue"   : "SC",
                "year"    : paperDict["year"]
            }

            paperMessages.append(paperMessage)

        message = {"papers": paperMessages}
        return json.dumps(message);

    @cherrypy.expose
    def getAllCitingPapersIncremental(self, *args, **kwargs):

        def runCommand():

            paperTitle                                = kwargs["title"];
            cherrypy.response.headers["Content-Type"] = "application/json"
            querier                                   = torScholar.TorScholarQuerier(self.commandLineArgs)
            papers                                    = dataCollector.getAllCitingPapersIncremental(paperTitle)
            paperMessages                             = []

            for paper in papers:

                paperMessage =                  \
                {                               \
                    "title"   : paper["title"], \
                    "authors" : "Z. DeVito, N. Joubert, F. Palacios, S. Oakley, M. Medina, M. Barrientos, E. Elsen, F. Ham, A. Aiken, K. Duraisamy, E. Darve, J. Alonso, P. Hanrahan", \
                    "venue"   : "SC",
                    "year"    : paper["year"]
                }

                paperMessages.append(paperMessage)


                partialMessage = \
                { \
                    "type":"partial", \
                    "paper": paperMessage, \
                    "stats": { \
                        "indexed": paper["numPapersProcessedCumulative"], \
                        "depth": paper["depth"], \
                        "duplicates": len(paperMessages) - paper["numPapersProcessedCumulative"], \
                    }, \
                }

                yield self.packetize(json.dumps(partialMessage));

            doneMessage = \
            { \
                "type":"meta",
                "data":"done"
            }

            yield self.packetize(json.dumps(doneMessage))

            resultMessage = \
            { \
                "type":"result",
                "papers": paperMessages
            }

            yield self.packetize(json.dumps(resultMessage));

        return runCommand();

class Root():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    _cp_config = \
    {
        "tools.staticdir.on"    : True,
        "tools.staticdir.dir"   : os.path.join(current_dir, "..", "www"),
        "tools.staticdir.index" : "index.html",
    }

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

if __name__ == "__main__":

    ## Parse Command Line Arguments
    parser = argparse.ArgumentParser(description="xcitedby.org backend")
    parser.add_argument("--env", metavar="env", action="store",
                        default="dev", help="Either dev for development (default) or prod for production.")
    parser.add_argument("--numTorInstances", dest="numTorInstances", type=int, action="store",
                       default=4,
                       help="The number of TOR instances to launch.")
    commandLineArgs = parser.parse_args()

    if commandLineArgs.env == "dev":
        print
        print "Parsed commandline arguments:"
        print commandLineArgs
        print

    ## Configure TOR utils
    torUtils.torInitializeActiveInstanceIds(commandLineArgs)

    ## Configure server hierarchy
    root = Root()
    root.data = API(commandLineArgs);

    ## Setup Environment
    if commandLineArgs.env == "prod":
        cherrypy.config.update({"environment": "production",
                                "log.error_file": "site.log",
                                "server.socket_port": 61337});
        cherrypy.engine.redirectexceptions = RedirectExceptions(cherrypy.engine);
        cherrypy.engine.redirectexceptions.subscribe();

    cherrypy.config.update({
        'checker.on': False,
        'response.stream': True,
        });

    ## Start the server
    cherrypy.tree.mount(root, config=None)
    cherrypy.engine.start()
    cherrypy.engine.block()
