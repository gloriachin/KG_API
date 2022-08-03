CREATE CONSTRAINT FOR (g:Gene) REQUIRE g.Symbol IS UNIQUE;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS
FROM 'file:///edges_test.csv' AS row

MERGE (subject:Gene {Symbol: row.subject_symbol})
SET subject.ID = row.subject_id,
    subject.Prefixes = row.subject_id_prefixes,
    subject.Category = row.subject_category

MERGE (object:Gene {Symbol: row.object_symbol})
SET object.ID = row.object_id,
    object.Prefixes = row.object_id_prefixes,
    object.Category = row.object_category

CREATE (subject)-[p:ASSOCIATION]->(object)
SET p.Name = row.predicate,
    p.Publications = row.ASSOCIATION_Publications

;

// the following doesn't work because I get an error on the WHERE clause
//CREATE (subject)-[p:PHYSICALLY_INTERACTS_WITH]->(object)
//WHERE row.predicate CONTAINS 'physically interacts with'
//SET p.Publications = row.ASSOCIATION_Publications
