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
import socks
import socksipyhandler
import torUtils
import torConstants

class TorScholarQuerier(scholar.ScholarQuerier):
    """
    ProxyScholarQuerier instances can conduct a search on Google Scholar
    with subsequent parsing of the resulting HTML content and leveraging
    a randomly chosen web proxy from an input list of web proxies.
    """

    UA = "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9.2.9) Gecko/20100913 Firefox/3.6.9"

    def __init__(self, commandLineArgs):
        scholar.ScholarQuerier.__init__(self);
        self.commandLineArgs = commandLineArgs

    def query(self, search):
        """
        This method initiates a query with subsequent parsing of the
        response.
        """
        url = self.scholar_url % {'query': urllib.quote(search.encode('utf-8')), 'author': urllib.quote(self.author)}
        html = self._tryUrlReadWithTor(url)
        self.parse(html)

    def title(self, search):
        """
        This method initiates an allintitle search with subsequent parsing of the
        response.
        """
        url = self.TITLE_URL % {'title': urllib.quote(search.encode('utf-8'))}
        html = self._tryUrlReadWithTor(url)
        return self.parse(html)

    def citation(self, citation, page):
        """
        This method initiates a single query to the citation list of a paper
        """
        url = self.CITATION_URL % {'start': page*10, 'papernr': urllib.quote(citation)}
        html = self._tryUrlReadWithTor(url)
        return self.parse(html)

    def direct(self, url):
        """
        This method initiates a query with subsequent parsing of the
        response.
        """
        html = self._tryUrlReadWithTor(url)
        self.parse(html)

    def _tryUrlReadWithTor(self, url):

        torUtils.torUpdateActiveInstances()
        shuffledTorInstances = torUtils.torGetActiveInstanceIdsShuffled()

        for i in shuffledTorInstances:

            try:
                socket.setdefaulttimeout(2)

                #determine_public_facing_ip_url             = "http://www.networksecuritytoolkit.org/nst/tools/ip.php"
                #determine_public_facing_ip_source_no_proxy = urllib.urlopen(determine_public_facing_ip_url).read()

                socksPort                         = torConstants.TOR_BASE_SOCKS_PORT + i
                opener                            = urllib2.build_opener(socksipyhandler.SocksiPyHandler(socks.PROXY_TYPE_SOCKS4, '127.0.0.1', socksPort))
                opener.addheaders                 = [("User-agent", self.UA)]

                #determine_public_facing_ip_source = opener.open(determine_public_facing_ip_url).read()

                #if determine_public_facing_ip_source_no_proxy == determine_public_facing_ip_source:
                #    raise Exception                                                              \
                #        (                                                                      + \
                #            "[TORSCHOLAR ERROR] Public facing IP without TOR "                 + \
                #            "(" + determine_public_facing_ip_source_no_proxy.strip("\n") + ")" + \
                #            " matches public facing IP with TOR"                               + \
                #            "(" + determine_public_facing_ip_source.strip("\n") + ")."
                #        )

                return opener.open(url).read()

            except (urllib2.URLError, urllib2.HTTPError), e:
                print "[TORSCHOLAR ERROR] urllib2 error: " + str(e)
                torUtils.torMarkInstanceAsInactive(i)
            except Exception, e:
                print "[TORSCHOLAR ERROR] Exception: " + str(e)
                torUtils.torMarkInstanceAsInactive(i)

        raise Exception("[TORSCHOLAR ERROR] Couldn't connect to any TOR proxy.")
