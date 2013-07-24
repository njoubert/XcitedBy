"""
This module gets a list of proxy servers from hidemyass.com
"""

import urllib2
import lxml
import lxml.html
import re
import socket

def getProxiesHideMyAss():
    """
    This function gets a list of proxies from hidemyass.com
    """

    url           = "http://hidemyass.com/proxy-list"
    source        = urllib2.urlopen(url).read()
    source_xpath  = lxml.html.fromstring(source)
    edited_source = source

    for style_info in source_xpath.xpath('//style/text()'): 

        for style_info_line in style_info.split("\n"):
         
            match = re.match(r".(.*?){(.*?)}", style_info_line)
            
            if match:
                class_text    = 'class="' + match.group(1) + '"'
                style_text    = 'style="' + match.group(2) + '"'
                edited_source = edited_source.replace(class_text, style_text)

                

    edited_source_xpath = lxml.html.fromstring(edited_source)
    proxies             = []

    for tr in edited_source_xpath.xpath('//tr'):
        
        proxy_candidate_array           = tr.xpath("td[2]//*[not(contains(@style,'display:none'))]/text() | td[3]/text()")
        anonimity_string                = tr.xpath("td[8]/text() | td[7]/text()")
        proxy_candidate_ip_string       = ".".join(proxy_candidate_array) 
        proxy_candidate_ip_string_clean = re.sub(r"\.+",'.', re.sub(r"\.\n",":",proxy_candidate_ip_string))
        proxy_ip_string                 = re.findall( r'(([0-9]+(?:\.[0-9]+){3}))+(.*)', proxy_candidate_ip_string_clean)
        
        if (len(proxy_ip_string)):
            ip_string = ''.join(proxy_ip_string[0][1] + proxy_ip_string[0][2])
            proxies.append({"ip" : ip_string, "anonimity" : anonimity_string })



    determine_public_facing_ip_url = "http://www.networksecuritytoolkit.org/nst/tools/ip.php"
    cleaned_proxies                = []

    for proxy in proxies:
        
        proxy_ip = proxy["ip"]

        try:
            socket.setdefaulttimeout(3)
            proxy_handler                     = urllib2.ProxyHandler({"http": proxy_ip})
            proxy_auth_handler                = urllib2.ProxyBasicAuthHandler()
            request                           = urllib2.build_opener(proxy_handler, proxy_auth_handler)
            request.addheaders                = [("User-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; en) Opera 9.50")]
            determine_public_facing_ip_source = request.open(determine_public_facing_ip_url).read()

            if not determine_public_facing_ip_source.strip("\n") in proxy_ip:
                raise Exception( "Public facing IP (" + determine_public_facing_ip_source.strip("\n") + ") did not match the IP in the proxy list (" + proxy_ip + ")." )
            
            cleaned_proxies.append(proxy)

        except (urllib2.URLError, urllib2.HTTPError), e:
            print "urllib2 error: " + str(e)
        except Exception, e:
            print "Exception: " + str(e)

    return cleaned_proxies

def getProxiesMyPrivateProxy():
    """
    This function gets a list of proxies from myprivateproxy.com
    """

    f = open("../data/myprivateproxy.txt", "r")
    lines = f.readlines()
    tokengroups = [ re.split(":", line.strip()) for line in lines if line.strip() != "" ]
    proxies = [ { "ip" : "http://" + tokengroup[2] + ":" + tokengroup[3] + "@" + tokengroup[0] + ":" + tokengroup[1] } for tokengroup in tokengroups ]
    
    return proxies