CREATE CONSTRAINT FOR (s:Gene) REQUIRE s.ID IS UNIQUE;
CREATE CONSTRAINT FOR (o:Gene) REQUIRE o.ID IS UNIQUE;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS
FROM 'file:///gene_gene_formatted.csv' AS row

MERGE (s:Gene {ID: row.'Subject.id'})
SET s.Symbol = row.'Subject.symbol',
    s.Prefixes = row.'Subject.id prefixes'

MERGE (o:Gene {ID: row.'object.id'})
SET o.Symbol = row.'object.symbol',
    o.Prefixes = row.'object.id prefixes'

MERGE (s)-[p:PHYSICALLY_INTERACTS_WITH]->(o)
WHERE row.'ASSOCIATION.Predicate' ...?

// or I could do:

MERGE (s)-[p:ASSOCIATION {name: 'PHYSICALLY INTERACTS WITH'}]->(o)
WHERE ...?