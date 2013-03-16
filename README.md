Transitive Closure of a paper's Citation Graph
==============================================

Compute the transitive closure of the Google Scholar citation graph for a given paper

Caveats:

Since Google does not have an API, we have to scrape the page. That sucks, because they also throttle and ban you when you're just getting going nicely on your paper graph search traversal.  We try to limit this a little bit by waiting 1 second between requests.

Also, notice the commit timestamps for this project - midnight through 7am. 

This is research-level code. Tread carefully.

##TODO

- Try to make Google return more than 10 results per page, so we don't have to scrape as many pages
- Infer whether there is a next page from the current page, rather than blindly make a request for the next page until it runs out of content.

##Different approaches to consider

1. Rather than computing all of this, we can do it level-by-level as the user clicks to reveal a paper's sub-papers.

2. Maybe we can do the whole thing in the browser? Although there is probably no advantage because of Javascript XSS restrictions.

## Authors

- Mike Roberts
- Niels Joubert