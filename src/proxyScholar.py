"""
This module provides classes for querying Google Scholar and parsing
returned results using a randomly selected proxy server.  
"""

import urllib
import urllib2
import scholar
import random
import copy
import socket

class ProxyScholarQuerier(scholar.ScholarQuerier):
    """
    ProxyScholarQuerier instances can conduct a search on Google Scholar
    with subsequent parsing of the resulting HTML content and leveraging
    a randomly chosen web proxy from an input list of web proxies.
    """

    #UA = 'Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9.2.9) Gecko/20100913 Firefox/3.6.9'

    #class Parser(ScholarParser120726):
    #    def __init__(self, querier):
    #        ScholarParser.__init__(self)
    #        self.querier = querier

    #    def handle_article(self, art):
    #        return self.querier.add_article(art)

    #def __init__(self, author='', scholar_url=None, count=0):
    #    self.articles = []
    #    self.author = author
    #    # Clip to 100, as Google doesn't support more anyway
    #    self.count = min(count, 100)

    #    if author == '':
    #        self.scholar_url = self.NOAUTH_URL
    #    else:
    #        self.scholar_url = scholar_url or self.SCHOLAR_URL

    #    if self.count != 0:
    #        self.scholar_url += '&num=%d' % self.count

    def __init__(self, proxies):
        self.proxies = proxies
        scholar.ScholarQuerier.__init__(self);

    def query(self, search):
        """
        This method initiates a query with subsequent parsing of the
        response.
        """
        url = self.scholar_url % {'query': urllib.quote(search.encode('utf-8')), 'author': urllib.quote(self.author)}
        html = self._tryUrlReadWithProxy(url)
        self.parse(html)

    def title(self, search):
        """
        This method initiates an allintitle search with subsequent parsing of the
        response.
        """
        url = self.TITLE_URL % {'title': urllib.quote(search.encode('utf-8'))}
        html = self._tryUrlReadWithProxy(url)
        return self.parse(html)

    def citation(self, citation, page):
        """
        This method initiates a single query to the citation list of a paper
        """
        url = self.CITATION_URL % {'start': page*10, 'papernr': urllib.quote(citation)}
        html = self._tryUrlReadWithProxy(url)
        return self.parse(html)

    def direct(self, url):
        """
        This method initiates a query with subsequent parsing of the
        response.
        """
        html = self._tryUrlReadWithProxy(url)
        self.parse(html)

    def _tryUrlReadWithProxy(self, url):

        shuffledProxies = copy.deepcopy(self.proxies)
        random.shuffle(shuffledProxies)

        for proxy in shuffledProxies:
            
            proxy_ip = proxy["ip"]

            try:
                socket.setdefaulttimeout(3)

                determine_public_facing_ip_url    = "http://www.networksecuritytoolkit.org/nst/tools/ip.php"
                proxy_handler                     = urllib2.ProxyHandler({"http": proxy_ip})
                proxy_auth_handler                = urllib2.ProxyBasicAuthHandler()
                request                           = urllib2.build_opener(proxy_handler, proxy_auth_handler)
                request.addheaders                = [("User-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; en) Opera 9.50")]
                determine_public_facing_ip_source = request.open(determine_public_facing_ip_url).read()

                if not determine_public_facing_ip_source.strip("\n") in proxy_ip:
                    raise Exception( "Public facing IP (" + determine_public_facing_ip_source.strip("\n") + ") did not match the IP in the proxy list (" + proxy_ip + ")." )

                proxy_handler                     = urllib2.ProxyHandler({"http": proxy_ip})
                proxy_auth_handler                = urllib2.ProxyBasicAuthHandler()
                request                           = urllib2.build_opener(proxy_handler, proxy_auth_handler)
                request.addheaders                = [("User-agent", self.UA)]
                return request.open(url).read()

            except (urllib2.URLError, urllib2.HTTPError), e:
                print "urllib2 error: " + str(e)
            except Exception, e:
                print "Exception: " + str(e)

        print "ERROR: Ran out of proxies."
