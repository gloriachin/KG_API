CREATE CONSTRAINT FOR (g:Gene) REQUIRE g.Symbol IS UNIQUE;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS
FROM 'file:///clean_gene_gene.csv' AS row

MERGE (subject:Gene {Symbol: row.subject_symbol})
SET subject.ID = row.subject_id,
    subject.Prefixes = row.subject_id_prefixes

MERGE (object:Gene {Symbol: row.object_symbol})
SET object.ID = row.object_id,
    object.Prefixes = row.object_id_prefixes

CREATE (subject)-[p:ASSOCIATION]->(object)
SET p.Name = row.predicate,
    p.Publications = row.ASSOCIATION_Publications

;