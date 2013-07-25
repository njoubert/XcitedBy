import cherrypy

import scholar

import proxyListGetter
import proxyScholar
import dataCollector

import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

# class form_response_page:

#     @cherrypy.expose
#     def index(self, *args, **kwargs):
#         papertitle = kwargs['paper_name']

#         proxies = proxyListGetter.getProxiesMyPrivateProxy()
#         querier = proxyScholar.ProxyScholarQuerier(proxies)
#         papersDict = dataCollector.getAllPapers(papertitle, querier)

#         papersSorted = sorted(papersDict.iteritems(), key=lambda x: x[1][0]['num_citations'], reverse=True)

#         html = "<html><head></head><body>"
#         html = html + "<h1>Citation Search Results</h1>"
#         html = html + "<h3>" + str(len(papersSorted)) + " papers cited (directly or indirectly) \"" + papertitle + "\"</h3>"
#         html = html + "<table>"
#         for t,pair in papersSorted:
#             a, depth = pair
#             year = str(a['year']) if a['year'] else "-"
#             url_citations = a['url_citations'] if a['url_citations'] else "#"
#             num_citations = str(a['num_citations']) if a['num_citations'] else "0"
#             url = a['url'] if a['url'] else "#"
#             html = html + "<tr><td><a href='" + url_citations + "'> "+ num_citations + " Citations</a></td><td>" + str(depth) + " Deep</td><td>" + year + "</td><td><a href='"+ url +"'>" + t + "</a></td></tr>"
#         html = html + "</table></body></html>"
#         return html

class root_page(object):
    _cp_config = {'tools.staticdir.on' : True,
                  'tools.staticdir.dir' : os.path.join(current_dir, 'public'),
                  'tools.staticdir.index' : 'index.html',
    }

    
    @cherrypy.expose
    def checkPaper(self, *args, **kwargs):

        return "HESSS";






cherrypy.quickstart(root_page())