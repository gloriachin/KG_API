CREATE CONSTRAINT gene_constraint FOR (g:Gene) REQUIRE g.Symbol IS UNIQUE;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/edges_test_underscores.csv' AS row

MERGE (subject:Gene {Symbol: row.subject_symbol})
SET subject.ID = row.subject_id,
    subject.Prefixes = row.subject_id_prefixes,
    subject.Category = row.subject_category

MERGE (object:Gene {Symbol: row.object_symbol})
SET object.ID = row.object_id,
    object.Prefixes = row.object_id_prefixes,
    object.Category = row.object_category

CREATE (subject)-[p:ASSOCIATED_WITH]->(object)
SET p.Publications = row.ASSOCIATION_Publications,
    p.Predicate = row.predicate 

;

// The goal would be to do something like:
    // CREATE (subject)-[p:PHYSICALLY_INTERACTS_WITH]->(object)
    // WHERE row.predicate = 'physically interacts with'
    // SET p.Publications = row.ASSOCIATION_Publications