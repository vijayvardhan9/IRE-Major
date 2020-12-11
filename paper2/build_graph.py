# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/
import networkx as nx
import sys
import json
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"
G_freq = nx.Graph()
G_pagerank = nx.DiGraph()

def build_query(entity_id):
    query = """SELECT ?wdLabel ?wd ?ooLabel ?o
    WHERE {
    VALUES (?s) {(wd:"""+ str(entity_id)+""")}
    ?s ?wdt ?o .
    ?wd wikibase:directClaim ?wdt .
    ?wd rdfs:label ?wdLabel .
    OPTIONAL {
    ?o rdfs:label ?oLabel .
    FILTER (lang(?oLabel) = "en")
    }
    FILTER (lang(?wdLabel) = "en")
    BIND (COALESCE(?oLabel, ?o) AS ?ooLabel)
    } ORDER BY xsd:integer(STRAFTER(STR(?wd), "http://www.wikidata.org/entity/P"))"""

    return query

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


with open(sys.argv[1], "r") as write_file:
    domain_list = json.load(write_file)
    i = 0
    for domain_item in domain_list:
        item_id = domain_item['item'][31:]
        quer = build_query(item_id)
        results = get_results(endpoint_url, quer)
        for result in results["results"]["bindings"]:
            # if result['o']['type'] == 'uri':
            #     o = 
            #     print(o)
            # else:
            #     o = 'nil'  
            if len(result['o']['value'].split('/entity/')) == 2:
                o = result['o']['value'].split('/entity/')[1]
                # if not G_pagerank.has_node(s):
                #     G_pagerank.add_node(s)
                # if not G_pagerank.has_node(o):
                #     G_pagerank.add_node(o)
                G_pagerank.add_edge(item_id,o)
            else:
                o = result['o']['value']
                o = o.replace(" ", "-")
            p = result['wd']['value'][31:]

            G_freq.add_edge(p,o)
        i += 1
        if i == 3000:
            break
        
    nx.write_edgelist(G_pagerank, "pagerank_graph.edgelist")
    nx.write_edgelist(G_freq, "freq_graph.edgelist")