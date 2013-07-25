import cherrypy
import json

import scholar
import torScholar

import os
import os.path


XCITEDBY_USER                = "mike"
TOR_EXECUTABLE_ABSOLUTE_PATH = "/Users/" + XCITEDBY_USER + "/xcitedby/TorBrowser_en-US.app/Contents/MacOS/tor"
TOR_TMP_ABSOLUTE_PATH        = "/Users/" + XCITEDBY_USER + "/xcitedby/tmp/tor/"
TOR_DATA_ABSOLUTE_BASE_PATH  = TOR_TMP_ABSOLUTE_PATH + "data/"
TOR_PID_ABSOLUTE_PATH        = TOR_TMP_ABSOLUTE_PATH + "pid/"
NUM_TOR_INSTANCES            = 4
TOR_BASE_CONTROL_PORT        = 8118
TOR_BASE_SOCKS_PORT          = 9050



current_dir = os.path.dirname(os.path.abspath(__file__))



class root_page(object):
    _cp_config = \
    {
        'tools.staticdir.on'    : True,
        'tools.staticdir.dir'   : os.path.join(current_dir, '..', 'www'),
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



def torStart():

    for i in range(NUM_TOR_INSTANCES):
        torDataAbsolutePath = TOR_DATA_ABSOLUTE_BASE_PATH + "tor%02d/" % i
        if not os.path.exists(torDataAbsolutePath):
            print "[MKDIR] " + torDataAbsolutePath
            os.makedirs(torDataAbsolutePath)

    if not os.path.exists(TOR_PID_ABSOLUTE_PATH):
        print "[MKDIR] " + TOR_PID_ABSOLUTE_PATH
        os.makedirs(TOR_PID_ABSOLUTE_PATH)

    for i in range(NUM_TOR_INSTANCES):
        controlPort            = TOR_BASE_CONTROL_PORT + i
        socksPort              = TOR_BASE_SOCKS_PORT   + i
        torPidFileAbsolutePath = TOR_PID_ABSOLUTE_PATH       + "tor%02d.pid" % i
        torDataAbsolutePath    = TOR_DATA_ABSOLUTE_BASE_PATH + "tor%02d/"    % i

        command = \
            "%s --RunAsDaemon 1 --ControlPort %d --SocksPort %d --PidFile %s --DataDirectory %s" % \
            (TOR_EXECUTABLE_ABSOLUTE_PATH, controlPort, socksPort, torPidFileAbsolutePath, torDataAbsolutePath)

        print "[COMMAND] " + command
        os.system(command)

def torStop():

    command = "killall tor"
    print "[COMMAND] " + command
    os.system(command)



torStop()
torStart()
cherrypy.quickstart(root_page())
torStop()
