from rdflib import Graph

g = Graph()

g.parse("src/temp/Person - Birth and Death.ttl", format="turtle")

rows = g.query("""
    select ?class_name
    where { 
        ?shape a sh:NodeShape ;
        sh:name ?class_name .
    }
""")


for row in rows:
    if isinstance(row, bool): continue
    print(row[0])
    print(row.asdict()['class_name'])