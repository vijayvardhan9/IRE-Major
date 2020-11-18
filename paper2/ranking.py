import sys
import networkx as nx
from operator import itemgetter 
from SPARQLWrapper import SPARQLWrapper, JSON 

G_freq = nx.read_edgelist("freq_graph.edgelist")
G_pagerank = nx.read_edgelist("pagerank_graph.edgelist")
endpoint_url = "https://query.wikidata.org/sparql"

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

pr = nx.pagerank(G_pagerank)
deg = nx.degree_centrality(G_freq)
query = build_query(sys.argv[1])
results = get_results(endpoint_url, query)

# rank_plus = {}
# rank_mult = {}
image = ''
image_val = ''

for result in results['results']['bindings']:
    p_val = result['wdLabel']['value']
    o_val = result['ooLabel']['value']
    if p_val == 'image' or p_val == 'logo image':
        image = p_val
        image_val = o_val
    if len(result['o']['value'].split('/entity/')) == 2:
        o = result['o']['value'].split('/entity/')[1]
        prank = pr[o]
    else:
        prank = 0
    freq = deg[result['wd']['value'][31:]]
    result['rank_plus'] = (freq + prank)/2
    result['rank_mult'] = (freq * prank)
    result['pagerank'] = prank
    result['frequency'] = freq
   
sorted_rank_mult = sorted(results['results']['bindings'], key=itemgetter('rank_mult'),reverse = True)
sorted_rank_plus = sorted(results['results']['bindings'], key=itemgetter('rank_plus'),reverse = True)
sorted_freq = sorted(results['results']['bindings'], key=itemgetter('frequency'),reverse = True)
sorted_pgrnk = sorted(results['results']['bindings'], key=itemgetter('pagerank'),reverse = True)

method = int(sys.argv[2]) 

if method == 1:
    i = 0
    print("RANDOM ATTRIBUTE-VALUE SELECTION\n\n")
    print("{} - {}".format(image, image_val))
    for result in results['results']['bindings']:
        i += 1
        if i == 25:
            break
        else:
            print("{} - {}".format(result['wdLabel']['value'], result['ooLabel']['value']))      
elif method == 2:
    i = 0
    print("RANKx ATTRIBUTE-VALUE SELECTION\n\n")
    print("{} - {}".format(image, image_val))
    for result in sorted_rank_mult:
        i += 1
        if i == 25:
            break
        else:
            print("{} - {}".format(result['wdLabel']['value'], result['ooLabel']['value']))
elif method == 3:
    i = 0
    print("RANK+ ATTRIBUTE-VALUE SELECTION\n\n")
    print("{} - {}".format(image, image_val))
    for result in sorted_rank_plus:
        i += 1
        if i == 25:
            break
        else:
            print("{} - {}".format(result['wdLabel']['value'], result['ooLabel']['value']))
elif method == 4:
    i = 0
    print("PAGERANK ATTRIBUTE-VALUE SELECTION\n\n")
    print("{} - {}".format(image, image_val))
    for result in sorted_pgrnk:
        i += 1
        if i == 25:
            break
        else:
            print("{} - {}".format(result['wdLabel']['value'], result['ooLabel']['value']))
elif method == 5:
    i = 0
    print("FREQUENCY ATTRIBUTE-VALUE SELECTION\n\n")
    print("{} - {}".format(image, image_val)) 
    for result in sorted_freq:
        i += 1
        if i == 25:
            break
        else:
            print("{} - {}".format(result['wdLabel']['value'], result['ooLabel']['value']))    