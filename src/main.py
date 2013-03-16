import cherrypy

import dataCollector


class form_response_page:

    @cherrypy.expose
    def index(self, *args, **kwargs):
        papertitle = kwargs['paper_name']
        papersDict = dataCollector.getAllPapers(papertitle)

        papersSorted = sorted(papersDict.iteritems(), key=lambda x: x[1]['num_citations'], reverse=True)

        html = "<html><head></head><body>"
        html = html + "<h1>Citation Search Results</h1>"
        html = html + "<h3>" + str(len(papersSorted)) + " cited (directly or indirectly) \"" + papertitle + "\"</h3>"
        html = html + "<table>"
        for t,a in papersSorted:
            year = a['year'] if a['year'] else "-"
            html = html + "<tr><td><a href='" + a['url_citations'] + "'> "+ str(a['num_citations']) + " Citations</a></td><td>" + year + "</td><td><a href='"+a['url']+"'>" + t + "</a></td></tr>"
        html = html + "</table></body></html>"
        return html

class root_page:

    form_response = form_response_page()
    
    @cherrypy.expose
    def index(self):
        html = \
'''
<form action="/form_response/" method="POST">
    Enter the name of the paper here:
    <input type="textbox" name="paper_name" />
    <input type="submit">
</form>
'''
        return html



cherrypy.quickstart(root_page())