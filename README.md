Transitive Closure of a paper's Citation Graph
==============================================

Compute the transitive closure of the Google Scholar citation graph for a given paper

Caveats:

Since Google does not have an API, we have to scrape the page. That sucks, because they also throttle and ban you when you're just getting going nicely on your paper graph search traversal.  We try to limit this a little bit by waiting 1 second between requests.

Also, notice the commit timestamps for this project - midnight through 7am. 

This is research-level code. Tread carefully.

## Authors

- Mike Roberts
- Niels Joubert