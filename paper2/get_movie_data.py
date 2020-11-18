# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """#Movies released in 2017
SELECT DISTINCT ?item ?itemLabel WHERE {
  ?item wdt:P31 wd:Q11424.
  ?item wdt:P577 ?pubdate.
  FILTER((?pubdate >= "1950-01-01T00:00:00Z"^^xsd:dateTime) && (?pubdate <= "2000-12-31T00:00:00Z"^^xsd:dateTime))
  #FILTER (lang(?itemLabel) = "hi")
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result)