from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint

endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"

id='wd:Q9554'


sparql = SPARQLWrapper(endpoint)
sparql.setQuery(
    """
PREFIX bd: <http://www.bigdata.com/rdf#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX schema: <http://schema.org/> 
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX wikibase: <http://wikiba.se/ontology#> """
    +
"""
SELECT ?personLabel ?personDesc
WHERE {
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "fr" .
    """+ id +
    """ rdfs:label ?personLabel .
    
    """ + id +""" schema:description ?personDesc .
  }
}
""")  # Link to query: http://tinyurl.com/z8bd26h

sparql.setReturnFormat(JSON)

results = sparql.query().convert()

pprint(results)